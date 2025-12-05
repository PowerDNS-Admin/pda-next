from typing import List, Optional, Set, Tuple
from uuid import UUID

from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from models.enums import PrincipalTypeEnum, ResourceTypeEnum


class PermissionsManager:
    """Provides an interface for managing and validating permissions."""

    @staticmethod
    def permission_matches(required: str, granted: str) -> bool:
        return required == granted or required.startswith(f'{granted}:')

    @staticmethod
    async def expand_principal(redis: Redis, session: AsyncSession, principal_id: UUID,
                               use_cache: bool = True, ttl: int = 300) -> List[Tuple[str, Optional[UUID]]]:
        import json
        from loguru import logger
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
        from models.db.acl import Role, Principal

        key = f'acl:expansion:{principal_id}'

        if use_cache:
            cached = await redis.get(key)

            if cached:
                return [(pt, UUID(pid) if pid else None) for pt, pid in json.loads(cached)]

        stmt = select(Principal).options(selectinload(Principal.roles)).where(Principal.id == principal_id)

        principal: Optional[Principal] = (await session.execute(stmt)).scalar_one_or_none()

        if not principal:
            expanded = [(PrincipalTypeEnum.all.value, None)]
        else:
            results: Set[Tuple[str, Optional[UUID]]] = set()
            results.add((principal.type.value, principal.id))

            # include tenant if exists
            if principal.tenant_id:
                results.add((PrincipalTypeEnum.tenant.value, principal.tenant_id))

            # fetch roles associated with principal (both system-wide and tenant-specific)
            role_ids = [assoc.role_id for assoc in principal.roles]
            visited = set()

            async def walk_role(role_id: UUID):
                if role_id in visited:
                    return

                visited.add(role_id)

                stmt = select(Role).options(selectinload(Role.parents)).where(Role.id == role_id)

                role: Optional[Role] = (await session.execute(stmt)).scalar_one_or_none()

                if not role:
                    return

                # only include roles that are system-wide or match principal's tenant
                if role.tenant_id is None or role.tenant_id == principal.tenant_id:
                    results.add((PrincipalTypeEnum.role.value, role.id))
                # inherit parent roles recursively
                for inh in role.parents:
                    await walk_role(inh.parent_role_id)

            for rid in role_ids:
                await walk_role(rid)

            results.add((PrincipalTypeEnum.all.value, None))

            expanded = list(results)

        if use_cache:
            await redis.set(key, json.dumps([(pt, str(pid) if pid else None) for pt, pid in expanded]), ex=ttl)

        return expanded

    @staticmethod
    async def check_access(redis: Redis, session: AsyncSession, principal_id: UUID, tenant_id: Optional[UUID],
                           resource_type: ResourceTypeEnum, resource_id: Optional[UUID], required_permissions: List[str],
                           use_cache: bool = True, acl_version: str = '1', ttl: int = 60) -> bool:
        from loguru import logger
        from sqlalchemy import select, and_, or_
        from models.db.acl import Policy

        key = (f"acl:check:{principal_id}:{tenant_id}:{resource_type.value}:{resource_id}:"
               + f"{','.join(required_permissions)}:v{acl_version}")

        if use_cache:
            cached = await redis.get(key)

            if cached is not None:
                return cached == '1'

        expanded = await PermissionsManager.expand_principal(redis, session, principal_id, use_cache, ttl)

        principal_clauses = []

        for p_type, p_id in expanded:
            if p_id is None:
                principal_clauses.append(and_(Policy.principal_type == p_type, Policy.principal_id.is_(None)))
            else:
                principal_clauses.append(and_(Policy.principal_type == p_type, Policy.principal_id == p_id))

        stmt = select(Policy).where(
            Policy.resource_type == resource_type,
            or_(Policy.resource_id == resource_id, Policy.resource_id.is_(None)),
            or_(*principal_clauses),
            or_(Policy.tenant_id == tenant_id, Policy.tenant_id.is_(None))
        )

        policies = (await session.scalars(stmt)).all()

        print(stmt.compile(compile_kwargs={"literal_binds": True}))

        logger.warning(f'Resource Type: {resource_type} ({type(resource_type)})')
        logger.warning(f'Resource ID: {resource_id} ({type(resource_id)})')
        logger.warning(f'Principal ID: {principal_id} ({type(principal_id)})')
        logger.warning(f'Tenant ID: {tenant_id}')
        logger.warning(f'Principals: {expanded}')
        logger.warning(f'Policies: {policies}')

        result = True

        for perm in required_permissions:
            decision = None
            for pol in policies:
                if PermissionsManager.permission_matches(perm, pol.permission):
                    if pol.deny:
                        decision = False
                        break
                    else:
                        if decision is None:
                            decision = True
            if decision is False or decision is None:
                result = False

        if use_cache:
            await redis.set(key, '1' if result else '0', ex=ttl)

        return result

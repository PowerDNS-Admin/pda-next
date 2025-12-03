from uuid import UUID

from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from lib.permissions.definitions import Permission
from models.api.auth import Principal
from models.enums import ResourceTypeEnum


class PermissionsManager:
    """Provides an interface for managing and validating permissions."""

    @staticmethod
    async def has_permission(
            db: AsyncSession,
            redis: Redis,
            principal: Principal,
            resource_type: ResourceTypeEnum,
            resource_id: str | UUID,
            permissions: Permission | list[Permission],
    ) -> bool:
        """Verifies if the given principal has the given permission for the given resource."""
        from loguru import logger
        from sqlalchemy import select
        from models.db.acl import RolePrincipal, RolePermission, Policy

        if isinstance(resource_id, str):
            resource_id = UUID(resource_id)

        if isinstance(permissions, Permission):
            permissions = [permissions]

        permission_strings = set(p.uri for p in permissions)

        valid = False

        for uri in permission_strings:
            cache_key = f'permission:{principal.type.value}:{principal.id}:{resource_type.value}:{resource_id}:{uri}'

            # Check if permission is cached already
            cached = await redis.get(cache_key)

            # If permission is cached and still valid then extend the cache expiration
            if cached is not None and bool(int(cached)):
                await redis.set(cache_key, '1', ex=60)
                break

            # Check principal roles
            stmt = select(RolePrincipal.role_id).where(
                RolePrincipal.tenant_id == principal.tenant_id,
                RolePrincipal.principal_type == principal.type,
                RolePrincipal.principal_id == principal.id,
            )

            role_ids = (await db.execute(stmt)).scalars().all()

            stmt = select(RolePermission.permission).where(RolePermission.role_id.in_(role_ids))

            role_permissions = set((await db.execute(stmt)).scalars().all())

            if uri in role_permissions:
                valid = True
                await redis.set(cache_key, '1', ex=60)

                logger.trace(f'Principal Authorized (By Role): {principal.type.value}({principal.id}), '
                             + f'{resource_type.value}({resource_id}), permission: {uri}')

                break

            # Check principal policies
            stmt = select(Policy.id).where(
                Policy.resource_type == resource_type.value,
                Policy.resource_id == resource_id,
                Policy.principal_type == principal.type,
                Policy.principal_id == principal.id,
                Policy.permission == uri,
            )

            policy_id = (await db.execute(stmt)).scalar_one_or_none()

            if isinstance(policy_id, UUID):
                valid = True
                await redis.set(cache_key, '1', ex=60)

                logger.trace(f'Principal Authorized (By Policy): {principal.type.value}({principal.id}), '
                             + f'{resource_type.value}({resource_id}), permission: {uri}')

                break

            logger.critical(
                f'Principal Not Authorized: {principal.type.value}({principal.id}), {resource_type.value}({resource_id}), permission: {uri}')

            await redis.set(cache_key, '1' if valid else '0', ex=60)

        return valid

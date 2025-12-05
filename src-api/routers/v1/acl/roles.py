from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import Principal, ListParamsModel
from models.api.acl.roles import RolesSchema, RoleOutSchema, RoleInSchema
from routers.v1.acl import router


@router.post(
    '/roles',
    response_model=RolesSchema,
    summary='List ACL roles',
    description='Lists ACL roles for the current authentication context.',
    operation_id='acl:roles:list',
)
async def record_list(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RolesSchema:
    """List ACL roles"""
    from sqlalchemy import select, func
    from sqlalchemy.orm import selectinload
    from lib.sql import SqlQueryBuilder
    from models.db.acl import Role

    # Build a statement to retrieve the relevant records
    stmt = select(Role).options(selectinload(Role.principals))

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Role.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, Role)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return RolesSchema(
        records=[RoleOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
    )


@router.post(
    '/roles/create',
    response_model=RoleOutSchema,
    summary='Create ACL role',
    description='Creates ACL role for the current authentication context.',
    operation_id='acl:roles:create',
)
async def record_create(
        role: RoleInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RoleOutSchema:
    """Create ACL role"""
    from models.db.acl import Role, RolePrincipal

    # Create the record
    record = Role(
        slug=role.slug,
        description=role.description,
    )

    # Add the given principals to the role if any
    if role.principals:
        for principal in role.principals:
            # XXX: Consider validating the principal type / id combination to ensure valid data
            record.principals.append(RolePrincipal(
                tenant_id=principal.tenant_id if principal.tenant_id else role.tenant_id,
                principal_type=principal.principal_type,
                principal_id=principal.principal_id,
            ))

    # Enforce tenancy
    if principal.tenant_id:
        record.tenant_id = principal.tenant_id
    else:
        record.tenant_id = role.tenant_id

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record, attribute_names=['principals'])

    # Build the response
    return RoleOutSchema.model_validate(record)


@router.get(
    '/roles/{role_id}',
    response_model=RoleOutSchema,
    summary='Read ACL role',
    description='Read ACL role from the current authentication context.',
    operation_id='acl:roles:read',
)
async def record_read(
        role_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RoleOutSchema:
    """Read ACL role"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from models.db.acl import Role

    # Build a statement to retrieve the record
    stmt = select(Role).options(selectinload(Role.principals)).where(Role.id == role_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Role.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: Role | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Role {role_id} not found')

    # Build the response
    return RoleOutSchema.model_validate(record)


@router.patch(
    '/roles/{role_id}',
    response_model=RoleOutSchema,
    summary='Update ACL role',
    description='Update ACL role in the current authentication context.',
    operation_id='acl:roles:update',
)
async def record_update(
        role_id: UUID,
        role: RoleInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RoleOutSchema:
    """Update ACL role"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from models.db.acl import Role, RolePrincipal

    # Build a statement to retrieve the record
    stmt = select(Role).options(selectinload(Role.principals)).where(Role.id == role_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Role.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: Role | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Role {role_id} not found')

    # Update the record
    record.slug = role.slug
    record.description = role.description

    # Update associated principals if defined
    if isinstance(role.principals, list):
        existing_principals = set([r.principal_id for r in record.principals])
        updated_principals = set([r.principal_id for r in role.principals])

        # Remove existing principals that weren't retained
        for principal in list(record.principals):
            if principal.principal_id not in updated_principals:
                record.principals.remove(principal)

        # Add new principals that don't already exist
        for principal in role.principals:
            if principal.principal_id in existing_principals:
                continue
            # XXX: Consider validating the principal type / id combination to ensure valid data
            record.principals.append(RolePrincipal(
                tenant_id=principal.tenant_id if principal.tenant_id else role.tenant_id,
                principal_type=principal.principal_type,
                principal_id=principal.principal_id,
            ))

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record, attribute_names=['principals'])

    # Build the response
    return RoleOutSchema.model_validate(record)


@router.delete(
    '/roles/{role_id}',
    summary='Delete ACL role',
    description='Delete ACL role in the current authentication context.',
    operation_id='acl:roles:delete',
)
async def record_delete(
        role_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> None:
    """Delete ACL role"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.acl import Role

    # Build a statement to delete the record
    stmt = delete(Role).where(Role.id == role_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Role.tenant_id == principal.tenant_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Role {role_id} not found')

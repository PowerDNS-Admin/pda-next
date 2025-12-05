from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import Principal, ListParamsModel
from models.api.acl.policies import PoliciesSchema, PolicyOutSchema, PolicyInSchema
from routers.v1.acl import router


@router.post(
    '/policies',
    response_model=PoliciesSchema,
    summary='List ACL policies',
    description='Lists ACL policies for the current authentication context.',
    operation_id='acl:policies:list',
)
async def record_list(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> PoliciesSchema:
    """List ACL policies"""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.acl import Policy

    # Build a statement to retrieve the relevant records
    stmt = select(Policy)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Policy.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, Policy)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return PoliciesSchema(
        records=[PolicyOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
    )


@router.post(
    '/policies/create',
    response_model=PolicyOutSchema,
    summary='Create ACL policy',
    description='Create ACL policy for the current authentication context.',
    operation_id='acl:policies:create',
)
async def record_create(
        policy: PolicyInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> PolicyOutSchema:
    """Create ACL policy"""
    from models.db.acl import Policy

    # Create the record
    record = Policy(
        resource_type=policy.resource_type,
        resource_id=policy.resource_id,
        principal_type=policy.principal_type,
        principal_id=policy.principal_id,
        permission=policy.permission,
    )

    # Enforce tenancy
    if principal.tenant_id:
        record.tenant_id = principal.tenant_id
    else:
        record.tenant_id = policy.tenant_id

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return PolicyOutSchema.model_validate(record)


@router.get(
    '/policies/{policy_id}',
    response_model=PolicyOutSchema,
    summary='Read ACL policy',
    description='Read ACL policy from the current authentication context.',
    operation_id='acl:policies:read',
)
async def record_read(
        policy_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> PolicyOutSchema:
    """Read ACL policy"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.acl import Policy

    # Build a statement to retrieve the record
    stmt = select(Policy).where(Policy.id == policy_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Policy.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: Policy | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Policy {policy_id} not found')

    # Build the response
    return PolicyOutSchema.model_validate(record)


@router.patch(
    '/policies/{policy_id}',
    response_model=PolicyOutSchema,
    summary='Update ACL policy',
    description='Update ACL policy in the current authentication context.',
    operation_id='acl:policies:update',
)
async def record_update(
        policy_id: UUID,
        policy: PolicyInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> PolicyOutSchema:
    """Update ACL policy"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.acl import Policy

    # Build a statement to retrieve the record
    stmt = select(Policy).where(Policy.id == policy_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Policy.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: Policy | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Policy {policy_id} not found')

    # Update the record
    record.resource_type = policy.resource_type
    record.resource_id = policy.resource_id
    record.principal_type = policy.principal_type
    record.principal_id = policy.principal_id
    record.permission = policy.permission

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return PolicyOutSchema.model_validate(record)


@router.delete(
    '/policies/{policy_id}',
    summary='Delete ACL policy',
    description='Delete ACL policy from the current authentication context.',
    operation_id='acl:policies:delete',
)
async def record_delete(
        policy_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete ACL policy"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.acl import Policy

    # Build a statement to delete the record
    stmt = delete(Policy).where(Policy.id == policy_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Policy.tenant_id == principal.tenant_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Policy {policy_id} not found')

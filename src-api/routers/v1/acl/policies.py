from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import Principal
from routers.v1.acl import router


@router.get(
    '/policies',
    summary='List ACL policies',
    description='Lists ACL policies for the current authentication context.',
    operation_id='acl:policies:list',
)
async def record_list(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """List ACL policies"""


@router.post(
    '/policies',
    summary='Create ACL policy',
    description='Create ACL policy for the current authentication context.',
    operation_id='acl:policies:create',
)
async def record_create(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Create ACL policy"""


@router.get(
    '/policies/{policy_id}',
    summary='Read ACL policy',
    description='Read ACL policy from the current authentication context.',
    operation_id='acl:policies:read',
)
async def record_read(
        policy_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Read ACL policy"""


@router.patch(
    '/policies/{policy_id}',
    summary='Update ACL policy',
    description='Update ACL policy in the current authentication context.',
    operation_id='acl:policies:update',
)
async def record_update(
        policy_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Update ACL policy"""


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

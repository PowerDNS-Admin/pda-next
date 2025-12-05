from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.acl import router


@router.get(
    '/policies',
    summary='Retrieves all ACL policies',
    description='Retrieves all ACL policies for the current authentication context.',
    operation_id='acl:policies:all',
)
async def list_policies(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List ACL policies"""


@router.post(
    '/policies',
    summary='Creates a new ACL policy',
    description='Creates a new ACL policy for the current authentication context.',
    operation_id='acl:policies:create',
)
async def policy_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create an ACL policy"""


@router.get(
    '/policies/{policy_id}',
    summary='Retrieves an ACL policy',
    description='Retrieves an ACL policy from the current authentication context.',
    operation_id='acl:policies:read',
)
async def policy_read(
        policy_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read an ACL policy"""


@router.patch(
    '/policies/{policy_id}',
    summary='Updates an ACL policy',
    description='Updates an ACL policy in the current authentication context.',
    operation_id='acl:policies:update',
)
async def policy_update(
        policy_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update an ACL policy"""


@router.delete(
    '/policies/{policy_id}',
    summary='Deletes an ACL policy',
    description='Deletes an ACL policy from the current authentication context.',
    operation_id='acl:policies:delete',
)
async def policy_delete(
        policy_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete an ACL policy"""

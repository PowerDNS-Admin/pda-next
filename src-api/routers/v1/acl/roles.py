from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.acl import router


@router.get(
    '/roles',
    summary='Retrieves all ACL roles',
    description='Retrieves all ACL roles for the current authentication context.',
    operation_id='acl:roles:all',
)
async def list_roles(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List ACL roles"""


@router.post(
    '/roles',
    summary='Creates a new ACL role',
    description='Creates a new ACL role for the current authentication context.',
    operation_id='acl:roles:create',
)
async def role_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create an ACL role"""


@router.get(
    '/roles/{role_id}',
    summary='Retrieves an ACL role',
    description='Retrieves an ACL role from the current authentication context.',
    operation_id='acl:roles:read',
)
async def role_read(
        role_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read an ACL role"""


@router.patch(
    '/roles/{role_id}',
    summary='Updates an ACL role',
    description='Updates an ACL role in the current authentication context.',
    operation_id='acl:roles:update',
)
async def role_update(
        role_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update an ACL role"""


@router.delete(
    '/roles/{role_id}',
    summary='Deletes an ACL role',
    description='Deletes an ACL role in the current authentication context.',
    operation_id='acl:roles:delete',
)
async def role_delete(
        role_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete an ACL role"""

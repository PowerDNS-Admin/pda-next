from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.keys import router


@router.get(
    '/tsig-keys',
    summary='Retrieves all ACL policies',
    description='Retrieves all ACL policies for the current authentication context.',
    operation_id='keys:tsig_keys:all',
)
async def list_tsig_keys(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List ACL policies"""


@router.post(
    '/tsig-keys',
    summary='Creates a new TSIG key',
    description='Creates a new TSIG key for the current authentication context.',
    operation_id='keys:tsig_keys:create',
)
async def tsig_key_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create a TSIG key"""


@router.get(
    '/tsig-keys/{id}',
    summary='Retrieves a TSIG key',
    description='Retrieves a TSIG key from the current authentication context.',
    operation_id='keys:tsig_keys:read',
)
async def tsig_key_read(
        id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read a TSIG key"""


@router.patch(
    '/tsig-keys/{id}',
    summary='Updates a TSIG key',
    description='Updates a TSIG key in the current authentication context.',
    operation_id='keys:tsig_keys:update',
)
async def tsig_key_update(
        id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update a TSIG key"""


@router.delete(
    '/tsig-keys/{id}',
    summary='Deletes a TSIG key',
    description='Deletes a TSIG key from the current authentication context.',
    operation_id='keys:tsig_keys:delete',
)
async def tsig_key_delete(
        id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete a TSIG key"""

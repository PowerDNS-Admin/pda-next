from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.keys import router


@router.get(
    '/crypto-keys',
    summary='Retrieves all crypto keys',
    description='Retrieves all crypto keys for the current authentication context.',
    operation_id='keys:crypto_keys:all',
)
async def list_crypto_keys(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List crypto keys"""


@router.post(
    '/crypto-keys',
    summary='Creates a new crypto key',
    description='Creates a new crypto key for the current authentication context.',
    operation_id='keys:crypto_keys:create',
)
async def crypto_key_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create a crypto key"""


@router.get(
    '/crypto-keys/{id}',
    summary='Retrieves a crypto key',
    description='Retrieves a crypto key from the current authentication context.',
    operation_id='keys:crypto_keys:read',
)
async def crypto_key_read(
        id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read a crypto key"""


@router.patch(
    '/crypto-keys/{id}',
    summary='Updates a crypto key',
    description='Updates a crypto key in the current authentication context.',
    operation_id='keys:crypto_keys:update',
)
async def crypto_key_update(
        id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update a crypto key"""


@router.delete(
    '/crypto-keys/{id}',
    summary='Deletes a crypto key',
    description='Deletes a crypto key in the current authentication context.',
    operation_id='keys:crypto_keys:delete',
)
async def crypto_key_delete(
        id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete a crypto key"""

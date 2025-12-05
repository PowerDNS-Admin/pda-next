from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.servers import router


@router.get(
    '/auto-primaries',
    summary='Retrieves all auto-primaries',
    description='Retrieves all auto-primaries for the current authentication context.',
    operation_id='servers:auto_primaries:all',
)
async def list_auto_primaries(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List auto-primaries"""


@router.post(
    '/auto-primaries',
    summary='Creates a new auto-primary',
    description='Creates a new auto-primary for the current authentication context.',
    operation_id='servers:auto_primaries:create',
)
async def auto_primary_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create an auto-primary"""


@router.get(
    '/auto-primaries/{auto_primary_id}',
    summary='Retrieves an auto-primary',
    description='Retrieves an auto-primary from the current authentication context.',
    operation_id='servers:auto_primaries:read',
)
async def auto_primary_read(
        auto_primary_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read an auto-primary"""


@router.patch(
    '/auto-primaries/{auto_primary_id}',
    summary='Updates an auto-primary',
    description='Updates an auto-primary in the current authentication context.',
    operation_id='servers:auto_primaries:update',
)
async def auto_primary_update(
        auto_primary_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update an auto-primary"""


@router.delete(
    '/auto-primaries/{auto_primary_id}',
    summary='Deletes an auto-primary',
    description='Deletes an auto-primary from the current authentication context.',
    operation_id='servers:auto_primaries:delete',
)
async def auto_primary_delete(
        auto_primary_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete an auto-primary"""

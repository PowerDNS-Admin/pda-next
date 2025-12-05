from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.zones import router


@router.get(
    '/recursive',
    summary='Retrieves all ACL policies',
    description='Retrieves all ACL policies for the current authentication context.',
    operation_id='zones:recursive:all',
)
async def list_rzones(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List recursive zones"""


@router.post(
    '/recursive',
    summary='Creates a new recusive zone',
    description='Creates a new recusive zone for the current authentication context.',
    operation_id='zones:recursive:create',
)
async def rzone_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create a recursive zone"""


@router.get(
    '/recursive/{zone_id}',
    summary='Retrieves a recursive zone',
    description='Retrieves a recursive zone from the current authentication context.',
    operation_id='zones:recursive:read',
)
async def rzone_read(
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read a recursive zone"""


@router.patch(
    '/recursive/{zone_id}',
    summary='Updates a recursive zone',
    description='Updates a recursive zone in the current authentication context.',
    operation_id='zones:recursive:update',
)
async def rzone_update(
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update a recursive zone"""


@router.delete(
    '/recursive/{zone_id}',
    summary='Deletes a recursive zone',
    description='Deletes a recursive zone from the current authentication context.',
    operation_id='zones:recursive:delete',
)
async def rzone_delete(
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete a recursive zone"""

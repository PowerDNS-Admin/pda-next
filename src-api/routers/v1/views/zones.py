from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.views import router


@router.get(
    '/{view_id}/zones',
    summary='Retrieves all view zones',
    description='Retrieves all view zones in the given zone.',
    operation_id='views:zones:all',
)
async def list_view_zones(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List view zones"""


@router.post(
    '/{view_id}/zones',
    summary='Creates a new view zone',
    description='Creates a new view zone in the given zone.',
    operation_id='views:zones:create',
)
async def zone_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create a view zone"""


@router.get(
    '/{view_id}/zones/{zone_id}',
    summary='Retrieves a view zone',
    description='Retrieves a view zone from the given zone.',
    operation_id='views:zones:read',
)
async def view_read(
        view_id:UUID,
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read a view zone"""


@router.patch(
    '/{view_id}/zones/{zone_id}',
    summary='Updates a view zone',
    description='Updates a view zone in the given zone.',
    operation_id='views:zones:update',
)
async def zone_update(
        view_id:UUID,
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update a view zone"""


@router.delete(
    '/{view_id}/zones/{zone_id}',
    summary='Deletes a view zone',
    description='Deletes a view in the current authentication context.',
    operation_id='views:zones:delete',
)
async def zone_delete(
        view_id:UUID,
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete a view zone"""

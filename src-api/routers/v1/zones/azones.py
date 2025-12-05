from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.zones import router


@router.get(
    '/authoritative',
    summary='Retrieves all authoritative zones',
    description='Retrieves all authoritative zones for the current authentication context.',
    operation_id='zones:authoritative:all',
)
async def list_azones(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List authoritative zones"""


@router.post(
    '/authoritative',
    summary='Creates a new authoritative zone',
    description='Creates a new authoritative zone for the current authentication context.',
    operation_id='zones:authoritative:create',
)
async def azone_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create an authoritative zone"""


@router.get(
    '/authoritative/{zone_id}',
    summary='Retrieves an authoritative zone',
    description='Retrieves an authoritative zone from the current authentication context.',
    operation_id='zones:authoritative:read',
)
async def azone_read(
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read an authoritative zone"""


@router.patch(
    '/authoritative/{zone_id}',
    summary='Updates an authoritative zone',
    description='Updates an authoritative zone in the current authentication context.',
    operation_id='zones:authoritative:update',
)
async def azone_update(
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update an authoritative zone"""


@router.delete(
    '/authoritative/{zone_id}',
    summary='Deletes an authoritative zone',
    description='Deletes an authoritative zone in the current authentication context.',
    operation_id='zones:authoritative:delete',
)
async def azone_delete(
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete an authoritative zone"""

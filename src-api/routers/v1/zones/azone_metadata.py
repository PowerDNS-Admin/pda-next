from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.zones import router


@router.get(
    '/authoritative/{zone_id}/metadata',
    summary='Retrieves all authoritative zone metadata',
    description='Retrieves all authoritative zone metadata in the given zone.',
    operation_id='zones:authoritative:metadata:all',
)
async def list_azone_metadata(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List authoritative zone metadata"""


@router.post(
    '/authoritative/{zone_id}/metadata',
    summary='Creates a new authoritative zone metadata',
    description='Creates a new authoritative zone metadata in the given zone.',
    operation_id='zones:authoritative:metadata:create',
)
async def azone_metadata_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create an authoritative zone metadata"""


@router.get(
    '/authoritative/{zone_id}/metadata/{metadata_id}',
    summary='Retrieves an authoritative zone metadata',
    description='Retrieves an authoritative zone metadata from the given zone.',
    operation_id='zones:authoritative:metadata:read',
)
async def azone_read(
        zone_id:UUID,
        metadata_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read an authoritative zone metadata"""


@router.patch(
    '/authoritative/{zone_id}/metadata/{metadata_id}',
    summary='Updates an authoritative zone metadata',
    description='Updates an authoritative zone metadata in the given zone.',
    operation_id='zones:authoritative:metadata:update',
)
async def azone_metadata_update(
        zone_id:UUID,
        metadata_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update an authoritative zone metadata"""


@router.delete(
    '/authoritative/{zone_id}/metadata/{metadata_id}',
    summary='Deletes an authoritative zone metadata',
    description='Deletes an authoritative zone in the current authentication context.',
    operation_id='zones:authoritative:metadata:delete',
)
async def azone_metadata_delete(
        zone_id:UUID,
        metadata_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete an authoritative zone metadata"""

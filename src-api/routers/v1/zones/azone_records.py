from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.zones import router


@router.get(
    '/authoritative/{zone_id}/records',
    summary='Retrieves all authoritative zone records',
    description='Retrieves all authoritative zone records in the given zone.',
    operation_id='zones:authoritative:records:all',
)
async def list_azone_records(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List authoritative zone records"""


@router.post(
    '/authoritative/{zone_id}/records',
    summary='Creates a new authoritative zone record',
    description='Creates a new authoritative zone record in the given zone.',
    operation_id='zones:authoritative:records:create',
)
async def azone_record_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create an authoritative zone record"""


@router.get(
    '/authoritative/{zone_id}/records/{record_id}',
    summary='Retrieves an authoritative zone record',
    description='Retrieves an authoritative zone record from the given zone.',
    operation_id='zones:authoritative:records:read',
)
async def azone_read(
        zone_id:UUID,
        record_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read an authoritative zone record"""


@router.patch(
    '/authoritative/{zone_id}/records/{record_id}',
    summary='Updates an authoritative zone record',
    description='Updates an authoritative zone record in the given zone.',
    operation_id='zones:authoritative:records:update',
)
async def azone_record_update(
        zone_id:UUID,
        record_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update an authoritative zone record"""


@router.delete(
    '/authoritative/{zone_id}/records/{record_id}',
    summary='Deletes an authoritative zone record',
    description='Deletes an authoritative zone in the current authentication context.',
    operation_id='zones:authoritative:records:delete',
)
async def azone_record_delete(
        zone_id:UUID,
        record_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete an authoritative zone record"""

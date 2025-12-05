from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.zones import router


@router.get(
    '/recursive/{zone_id}/records',
    summary='Retrieves all recursive zone records',
    description='Retrieves all recursive zone records in the given zone.',
    operation_id='zones:recursive:records:all',
)
async def list_rzone_records(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List recursive zone records"""


@router.post(
    '/recursive/{zone_id}/records',
    summary='Creates a new recursive zone record',
    description='Creates a new recursive zone record in the given zone.',
    operation_id='zones:recursive:records:create',
)
async def rzone_record_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create an recursive zone record"""


@router.get(
    '/recursive/{zone_id}/records/{record_id}',
    summary='Retrieves an recursive zone record',
    description='Retrieves an recursive zone record from the given zone.',
    operation_id='zones:recursive:records:read',
)
async def rzone_read(
        zone_id:UUID,
        record_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read an recursive zone record"""


@router.patch(
    '/recursive/{zone_id}/records/{record_id}',
    summary='Updates an recursive zone record',
    description='Updates an recursive zone record in the given zone.',
    operation_id='zones:recursive:records:update',
)
async def rzone_record_update(
        zone_id:UUID,
        record_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update an recursive zone record"""


@router.delete(
    '/recursive/{zone_id}/records/{record_id}',
    summary='Deletes an recursive zone record',
    description='Deletes an recursive zone in the current authentication context.',
    operation_id='zones:recursive:records:delete',
)
async def rzone_record_delete(
        zone_id:UUID,
        record_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete an recursive zone record"""

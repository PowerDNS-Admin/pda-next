from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api.auth import UserSchema, ClientSchema
from routers.root import router_responses

router = APIRouter(
    prefix='/zones',
    tags=['zones'],
    responses=router_responses,
)


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


@router.get(
    '/recursive',
    summary='Retrieves all ACL policies',
    description='Retrieves all ACL policies for the current authentication context.',
    operation_id='zones:recursive:all',
)
async def list_policies(
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

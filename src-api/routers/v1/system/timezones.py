from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.system import router


@router.get(
    '/timezones',
    summary='Retrieves all timezones',
    description='Retrieves all timezones.',
    operation_id='system:timezones:all',
)
async def list_timezones(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List timezones"""


@router.post(
    '/timezones',
    summary='Creates a new timezone',
    description='Creates a new timezone.',
    operation_id='system:timezones:create',
)
async def timezone_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create a timezone"""


@router.get(
    '/timezones/{id}',
    summary='Retrieves a timezone',
    description='Retrieves a timezone.',
    operation_id='system:timezones:read',
)
async def timezone_read(
        id: int,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read a timezone"""


@router.patch(
    '/timezones/{id}',
    summary='Updates a timezone',
    description='Updates a timezone.',
    operation_id='system:timezones:update',
)
async def timezone_update(
        id: int,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update a timezone"""


@router.delete(
    '/timezones/{id}',
    summary='Deletes a timezone',
    description='Deletes a timezone.',
    operation_id='system:timezones:delete',
)
async def timezone_delete(
        id: int,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete a timezone"""

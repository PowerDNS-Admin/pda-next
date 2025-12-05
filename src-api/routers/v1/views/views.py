from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.views import router


@router.get(
    '',
    summary='Retrieves all views',
    description='Retrieves all views for the current authentication context.',
    operation_id='views:all',
)
async def list_views(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List views"""


@router.post(
    '',
    summary='Creates a new view',
    description='Creates a new view for the current authentication context.',
    operation_id='views:create',
)
async def view_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create a view"""


@router.get(
    '/{view_id}',
    summary='Retrieves a view',
    description='Retrieves a view from the current authentication context.',
    operation_id='views:read',
)
async def view_read(
        view_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read a view"""


@router.patch(
    '/{view_id}',
    summary='Updates a view',
    description='Updates a view in the current authentication context.',
    operation_id='views:update',
)
async def view_update(
        view_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update a view"""


@router.delete(
    '/{view_id}',
    summary='Deletes a view',
    description='Deletes a view in the current authentication context.',
    operation_id='views:delete',
)
async def view_delete(
        view_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete a view"""

from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.views import router


@router.get(
    '/{view_id}/networks',
    summary='Retrieves all view network',
    description='Retrieves all view networks for the given view.',
    operation_id='views:networks:all',
)
async def list_view_networks(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List view network"""


@router.post(
    '/{view_id}/networks',
    summary='Creates a new view network',
    description='Creates a new view network for the given view.',
    operation_id='views:networks:create',
)
async def network_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create a view network"""


@router.get(
    '/{view_id}/networks/{network_id}',
    summary='Retrieves a view network',
    description='Retrieves a view network for the given view.',
    operation_id='views:networks:read',
)
async def network_read(
        view_id:UUID,
        network_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read a view network"""


@router.patch(
    '/{view_id}/networks/{network_id}',
    summary='Updates a view network',
    description='Updates a view network for the given view.',
    operation_id='views:networks:update',
)
async def network_update(
        view_id:UUID,
        network_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update a view network"""


@router.delete(
    '/{view_id}/networks/{network_id}',
    summary='Deletes a view network',
    description='Deletes a view network in the current authentication context.',
    operation_id='views:networks:delete',
)
async def network_delete(
        view_id:UUID,
        network_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete a view network"""

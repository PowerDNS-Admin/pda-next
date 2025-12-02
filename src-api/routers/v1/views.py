from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api.auth import UserSchema, ClientSchema
from routers.root import router_responses

router = APIRouter(
    prefix='/views',
    tags=['views'],
    responses=router_responses,
)


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

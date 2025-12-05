from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api.auth import UserSchema, ClientSchema
from routers.root import router_responses

router = APIRouter(
    prefix='/tenants',
    tags=['tenants'],
    responses=router_responses,
)


@router.get(
    '/tenants',
    summary='Retrieves all tenants',
    description='Retrieves all tenants.',
    operation_id='tenants:all',
)
async def list_tenants(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List tenants"""


@router.post(
    '/tenants',
    summary='Creates a new tenant',
    description='Creates a new tenant.',
    operation_id='tenants:create',
)
async def tenant_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create a tenant"""


@router.get(
    '/tenants/{tenant_id}',
    summary='Retrieves a tenant',
    description='Retrieves a tenant.',
    operation_id='tenants:read',
)
async def tenant_read(
        tenant_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read a tenant"""


@router.patch(
    '/tenants/{tenant_id}',
    summary='Updates a tenant',
    description='Updates a tenant.',
    operation_id='tenants:update',
)
async def tenant_update(
        tenant_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update a tenant"""


@router.delete(
    '/tenants/{tenant_id}',
    summary='Deletes a tenant',
    description='Deletes a tenant.',
    operation_id='tenants:delete',
)
async def tenant_delete(
        tenant_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete a tenant"""

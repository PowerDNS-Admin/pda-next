from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.system import router


@router.get(
    '/stopgap-domains',
    summary='Retrieves all stopgap domains',
    description='Retrieves all stopgap domains.',
    operation_id='system:stopgap_domains:all',
)
async def list_stopgap_domains(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List stopgap domains"""


@router.post(
    '/stopgap-domains',
    summary='Creates a new stopgap domain',
    description='Creates a new stopgap domain.',
    operation_id='system:stopgap_domains:create',
)
async def stopgap_domain_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create a stopgap domain"""


@router.get(
    '/stopgap-domains/{id}',
    summary='Retrieves a stopgap domain',
    description='Retrieves a stopgap domain.',
    operation_id='system:stopgap_domains:read',
)
async def stopgap_domain_read(
        id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read a stopgap domain"""


@router.patch(
    '/stopgap-domains/{id}',
    summary='Updates a stopgap domain',
    description='Updates a stopgap domain.',
    operation_id='system:stopgap_domains:update',
)
async def stopgap_domain_update(
        id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update a stopgap domain"""


@router.delete(
    '/stopgap-domains/{id}',
    summary='Deletes a stopgap domain',
    description='Deletes a stopgap domain.',
    operation_id='system:stopgap_domains:delete',
)
async def stopgap_domain_delete(
        id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete a stopgap domain"""

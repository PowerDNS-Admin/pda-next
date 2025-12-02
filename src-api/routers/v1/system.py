from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api.auth import UserSchema, ClientSchema
from routers.root import router_responses

router = APIRouter(
    prefix='/system',
    tags=['system'],
    responses=router_responses,
)


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

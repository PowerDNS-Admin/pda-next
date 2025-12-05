from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UserSchema, ClientSchema
from routers.v1.servers import router


@router.get(
    '',
    summary='Retrieves all servers',
    description='Retrieves all servers for the current authentication context.',
    operation_id='servers:all',
)
async def list_servers(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List servers"""


@router.post(
    '',
    summary='Creates a new server',
    description='Creates a new server for the current authentication context.',
    operation_id='servers:create',
)
async def server_create(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create a server"""


@router.get(
    '/{server_id}',
    summary='Retrieves a server',
    description='Retrieves a server from the current authentication context.',
    operation_id='servers:read',
)
async def server_read(
        server_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read a server"""


@router.patch(
    '/{server_id}',
    summary='Updates a server',
    description='Updates a server in the current authentication context.',
    operation_id='servers:update',
)
async def server_update(
        server_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update a server"""


@router.delete(
    '/{server_id}',
    summary='Deletes a server',
    description='Deletes a server in the current authentication context.',
    operation_id='servers:delete',
)
async def server_delete(
        server_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete a server"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api.auth import UserSchema, ClientSchema
from models.api.settings import SettingIn, SettingOut, SettingsOut
from routers.root import router_responses

router = APIRouter(
    prefix='/settings',
    tags=['settings'],
    responses=router_responses,
)


@router.get(
    '',
    response_model=SettingsOut,
    summary='Retrieves all settings',
    description='Retrieves all settings for the current authentication context.',
    operation_id='settings:all',
)
async def list_settings(
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """List settings"""


@router.post(
    '',
    response_model=SettingOut,
    summary='Creates a new setting override',
    description='Creates a new setting override for the tenant or user principals based on current authentication context.',
    operation_id='settings:create',
)
async def setting_create(
        setting: SettingIn,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Create a setting"""


@router.get(
    '/{key}',
    response_model=SettingOut,
    summary='Retrieves a setting',
    description='Retrieves a setting by key for the current authentication context.',
)
async def setting_read(
        key: str,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Read a setting"""


@router.patch(
    '/{key}',
    response_model=SettingOut,
    summary='Updates a setting',
    description='Updates a setting for the current authentication context.',
)
async def setting_update(
        key: str,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Update a setting"""


@router.delete(
    '/{key}',
    summary='Deletes a setting',
    description='Deletes a setting for the current authentication context.',
)
async def setting_delete(
        key: str,
        session: AsyncSession = Depends(get_db_session),
        principal: UserSchema | ClientSchema = Depends(get_principal),
):
    """Delete a setting"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Request, Response, Depends, Form, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_session_user, get_principal, authorize_oauth_client
from models.api import ListParamsModel
from models.api.auth import (
    Principal,
    UserSchema, UserAuthenticatorSchema, SessionSchema,
    UsersSchema, UserAuthenticatorsSchema, SessionsSchema,
)
from routers.root import router_responses

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses=router_responses,
)


@router.post('/token')
async def token(
        session: AsyncSession = Depends(get_db_session),
        client_id: UUID = Depends(authorize_oauth_client),
        scope: str = Form(None),
) -> dict:
    """Handle OAuth token grants."""
    from lib.settings import SettingsManager
    from lib.settings.definitions import sd
    from lib.api.oauth import create_access_token
    from models.db.auth import RefreshToken

    jwt_payload = {'sub': str(client_id)}

    if isinstance(scope, str):
        jwt_payload['scope'] = scope

    access_token_age = (await SettingsManager.get(session=session, key=sd.auth_access_token_age.key)).value
    refresh_token_age = (await SettingsManager.get(session=session, key=sd.auth_refresh_token_age.key)).value

    # Create the JWT access token
    access_token = create_access_token(payload=jwt_payload, age=access_token_age)

    # Create a refresh token
    refresh = await RefreshToken.create_token(session, refresh_token_age, client_id)

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'expires_in': access_token_age,
        'refresh_token': str(refresh.id),
    }


@router.post('/token/refresh')
async def token_refresh(
        grant_type: str = Form(...),
        client_id: str = Form(...),
        client_secret: str = Form(...),
        refresh_token: str = Form(...),
        scope: str = Form(None),
        session: AsyncSession = Depends(get_db_session),
):
    """Handle OAuth token grants."""
    from loguru import logger
    from lib.security import TokenGrantTypeEnum, TokenErrorTypeEnum
    from lib.settings import SettingsManager
    from lib.settings.definitions import sd
    from lib.api.oauth import create_access_token
    from models.db.auth import Client, RefreshToken

    # Retrieve the referenced client
    client = await Client.get_by_id(session, client_id)

    # Validate the client
    if not client or not client.verify_secret(client_secret):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, TokenErrorTypeEnum.invalid_client.value)

    if grant_type != TokenGrantTypeEnum.refresh_token.value:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, TokenErrorTypeEnum.unsupported_grant_type)

    # Retrieve the referenced token
    stored = await RefreshToken.get_by_id(session, refresh_token)

    # Validate the token
    if not stored or not stored.validate(client_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, TokenErrorTypeEnum.invalid_token.value)

    # Revoke the previous token
    await RefreshToken.revoke_token(session, stored)

    jwt_payload = {'sub': str(stored.user_id) if stored.user_id else client_id}

    if isinstance(scope, str):
        jwt_payload['scope'] = scope

    # TODO: Handle scope changes
    logger.critical('Token refresh endpoint needs permissions finished!')

    access_token_age = (await SettingsManager.get(session=session, key=sd.auth_access_token_age.key)).value
    refresh_token_age = (await SettingsManager.get(session=session, key=sd.auth_refresh_token_age.key)).value

    # Create the JWT access token
    access_token = create_access_token(payload=jwt_payload, age=access_token_age)

    # Create a refresh token
    refresh = await RefreshToken.create_token(session, refresh_token_age, client_id, stored.user_id)

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'expires_in': access_token_age,
        'refresh_token': str(refresh.id),
    }


@router.get('/session', response_model=Optional[UserSchema])
async def session(
        user: UserSchema = Depends(get_session_user),
) -> Optional[UserSchema]:
    return user


@router.post('/login', response_model=UserSchema)
async def login(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(get_db_session),
        username: str = Form(...),
        password: str = Form(...),
) -> UserSchema:
    from lib.tenants import TenantManager
    from lib.settings import SettingsManager
    from lib.settings.definitions import sd
    from models.db.auth import User, Session
    from models.enums import UserStatusEnum

    cookie_name = (await SettingsManager.get(session=session, key=sd.auth_session_cookie_name.key)).value
    cookie_age = (await SettingsManager.get(session=session, key=sd.auth_session_expiration_age.key)).value

    # Delete any existing session cookie
    response.delete_cookie(
        key=cookie_name,
        path='/',
        httponly=True,
        samesite='strict',
        secure=True,
    )

    if not username or isinstance(username, str) and not len(username.strip()):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'No username provided.')

    if not password or isinstance(password, str) and not len(password.strip()):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'No password provided.')

    # Identify the tenant ID (if any) based on request host
    tenant_id = await TenantManager.get_tenant_id_by_fqdn(session, request.headers.get('host'))

    # Attempt to retrieve a user from the database based on the given username
    db_user = await User.get_by_username(session, username, tenant_id)

    if not db_user or not db_user.verify_password(password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Invalid credentials provided.')

    # Ensure that the user has an appropriate status
    if db_user.status != UserStatusEnum.active:
        reason = 'This user is not active.'

        if db_user.status == UserStatusEnum.pending:
            reason = 'This user has not yet been invited.'

        if db_user.status == UserStatusEnum.invited:
            reason = 'This user has not yet been confirmed.'

        if db_user.status == UserStatusEnum.suspended:
            reason = 'This user has been suspended.'

        if db_user.status == UserStatusEnum.disabled:
            reason = 'This user has been disabled.'

        raise HTTPException(status.HTTP_401_UNAUTHORIZED, reason)

    # Update the user's last authentication timestamp
    await User.mark_authentication(session, db_user)

    # Create the user schema from the database user
    user = UserSchema.model_validate(db_user)

    # Create a new auth session for the user
    auth_session = await Session.create_session(session, user, request.client.host)

    response.set_cookie(
        key=cookie_name,
        value=auth_session.token,
        max_age=cookie_age,
        path='/',
        httponly=True,
        samesite='strict',
        secure=True,
    )

    return user


@router.get('/logout')
async def logout(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    from lib.settings import SettingsManager
    from lib.settings.definitions import sd
    from models.db.auth import Session

    cookie_name = (await SettingsManager.get(session=session, key=sd.auth_session_cookie_name.key)).value

    session_token = request.cookies.get(cookie_name)

    if session_token:
        db_session = await Session.get_by_token(session, session_token, request.client.host)
        if db_session:
            await Session.destroy_session(session, db_session.id)

    # Delete any existing session cookie
    response.delete_cookie(
        key=cookie_name,
        path='/',
        httponly=True,
        samesite='strict',
        secure=True,
    )

    return JSONResponse({'message': 'Successfully logged out.'})


@router.post(
    '/users',
    response_model=UsersSchema,
    summary='Get Users',
    description='Get all users in the current context.',
)
async def list_users(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> UsersSchema:
    """Gets all users in the current context."""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.auth import User

    stmt = select(User)

    if principal.tenant_id:
        stmt = stmt.where(User.tenant_id == principal.tenant_id)

    stmt_count = select(func.count()).select_from(stmt.subquery())

    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, User)

    records = (await session.execute(stmt)).scalars().all()

    result = UsersSchema(
        records=[UserSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
    )

    return result


@router.post(
    '/users/authenticators',
    response_model=UserAuthenticatorsSchema,
    summary='Get User Authenticators',
    description='Get all user authenticators in the current context.',
)
async def list_user_authenticators(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> UserAuthenticatorsSchema:
    """Gets all user authenticators in the current context."""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.auth import UserAuthenticator

    stmt = select(UserAuthenticator)

    if principal.tenant_id:
        stmt = stmt.where(UserAuthenticator.tenant_id == principal.tenant_id)

    stmt_count = select(func.count()).select_from(stmt.subquery())

    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, UserAuthenticator)

    records = (await session.execute(stmt)).scalars().all()

    result = UserAuthenticatorsSchema(
        records=[UserAuthenticatorSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
    )

    return result


@router.post(
    '/sessions',
    response_model=SessionsSchema,
    summary='Get User Sessions',
    description='Get all user sessions in the current context.',
)
async def list_sessions(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> SessionsSchema:
    """Gets all user sessions in the current context."""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.auth import Session

    stmt = select(Session)

    if principal.tenant_id:
        stmt = stmt.where(Session.tenant_id == principal.tenant_id)

    stmt_count = select(func.count()).select_from(stmt.subquery())

    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, Session)

    records = (await session.execute(stmt)).scalars().all()

    result = SessionsSchema(
        records=[SessionSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
    )

    return result

from uuid import UUID

from fastapi import APIRouter, Request, Response, Depends, Form, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, authorize_oauth_client
from models.api.auth import UserSchema
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
    from lib.security import ACCESS_TOKEN_AGE
    from lib.api.oauth import create_access_token
    from models.db.auth import RefreshToken

    jwt_payload = {'sub': str(client_id)}

    if isinstance(scope, str):
        jwt_payload['scope'] = scope

    # Create the JWT access token
    access_token = create_access_token(jwt_payload)

    # Create a refresh token
    refresh = await RefreshToken.create_token(session, ACCESS_TOKEN_AGE, client_id)

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'expires_in': ACCESS_TOKEN_AGE,
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
    from lib.security import ACCESS_TOKEN_AGE, TokenGrantTypeEnum, TokenErrorTypeEnum
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

    # Create the JWT access token
    access_token = create_access_token(jwt_payload)

    # Create a refresh token
    refresh = await RefreshToken.create_token(session, ACCESS_TOKEN_AGE, client_id, stored.user_id)

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'expires_in': ACCESS_TOKEN_AGE,
        'refresh_token': str(refresh.id),
    }


@router.post('/login', response_model=UserSchema)
async def login(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(get_db_session),
        username: str = Form(...),
        password: str = Form(...),
) -> UserSchema:
    from lib.security import COOKIE_NAME, SESSION_AGE
    from models.db.auth import User, Session
    from models.enums import UserStatusEnum

    # Delete any existing session cookie
    # FIXME: The following cookie delete isn't functioning
    response.delete_cookie(
        key=COOKIE_NAME,
        path='/',
        httponly=True,
        samesite='strict',
        secure=True,
    )

    if not username or isinstance(username, str) and not len(username.strip()):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'No username provided.')

    if not password or isinstance(password, str) and not len(password.strip()):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'No password provided.')

    # TODO: Implement tenant segregation

    # Attempt to retrieve a user from the database based on the given username
    db_user = await User.get_by_username(session, username)

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
        key=COOKIE_NAME,
        value=auth_session.token,
        max_age=SESSION_AGE,
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
    from lib.security import COOKIE_NAME
    from models.db.auth import Session

    session_token = request.cookies.get(COOKIE_NAME)

    if session_token:
        db_session = await Session.get_by_token(session, session_token, request.client.host)
        if db_session:
            await Session.destroy_session(session, db_session.id)

    # Delete any existing session cookie
    # FIXME: The following cookie delete isn't functioning
    response.delete_cookie(
        key=COOKIE_NAME,
        path='/',
        httponly=True,
        samesite='strict',
        secure=True,
    )

    return JSONResponse({'message': 'Successfully logged out.'})

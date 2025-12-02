from typing import AsyncGenerator
from uuid import UUID

from fastapi import Depends, Request, Form, HTTPException, status
from fastapi.security import HTTPBasicCredentials, SecurityScopes
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.oauth import oauth2_scheme, http_basic_scheme
from models.api.auth import UserSchema, ClientSchema


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    from app import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        yield session


async def get_principal(
        scopes: SecurityScopes,
        request: Request,
        session: AsyncSession = Depends(get_db_session),
        bearer_token: str = Depends(oauth2_scheme),
) -> UserSchema | ClientSchema:
    from datetime import datetime, timezone
    from jose import JWTError, jwt
    from loguru import logger
    from app import config
    from lib.security import ALGORITHM
    from lib.settings import SettingsManager
    from lib.settings.definitions import sd
    from models.db.auth import Session, Client

    required_scopes = set(scopes.scopes)

    # TODO: Implement support for granular resource level permissions
    logger.critical('Route principal helper needs permissions finished!')

    # Attempt OAuth Bearer Token Authentication
    if bearer_token:
        invalid_token_msg = 'Invalid bearer token'
        missing_scopes_msg = 'Client is not granted the required scopes.'
        try:
            payload = jwt.decode(bearer_token, config.app.secret_key, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, invalid_token_msg)

        if 'sub' not in payload or 'exp' not in payload:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, invalid_token_msg)

        client = await Client.get_by_id(session, payload['sub'])

        if not client:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, invalid_token_msg)

        # Verify that token hasn't expired
        if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], tz=timezone.utc):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, invalid_token_msg)

        if len(required_scopes) and 'scope' not in payload:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, missing_scopes_msg)

        granted_scopes = set(payload['scope'].split(' '))

        if not required_scopes.issubset(granted_scopes):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, missing_scopes_msg)

        return ClientSchema.model_validate(client)

    cookie_name = (await SettingsManager.get(session=session, key=sd.auth_session_cookie_name.key)).value

    # Attempt Session Token Authentication
    session_token = request.cookies.get(cookie_name)
    if session_token:
        # TODO: Implement hijack detection failsafe and terminate session if token matches but remote IP doesn't
        db_session = await Session.get_by_token(session, session_token, request.client.host)
        if db_session:
            # Extend the session's expiration timestamp
            await Session.extend_session(session, db_session)

            # TODO: Check if the associated user has the permissions listed in required_scopes

            return db_session.user

    # If neither works, raise an exception
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Not authenticated'
    )


async def authorize_oauth_client(
        credentials: HTTPBasicCredentials = Depends(http_basic_scheme),
        grant_type: str = Form(...),
        scope: str = Form(None),
        session: AsyncSession = Depends(get_db_session),
) -> UUID | Mapped[UUID]:
    from lib.security import TokenGrantTypeEnum, TokenErrorTypeEnum
    from models.db.auth import Client

    # Standard OAuth requires the grant_type field to be present in the body
    if grant_type != TokenGrantTypeEnum.client_credentials.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid grant_type provided. Must be "client_credentials".'
        )

    # Retrieve the referenced client
    client = await Client.get_by_id(session, credentials.username)

    # Validate the client
    if not client or not client.verify_secret(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TokenErrorTypeEnum.invalid_client.value,
            headers={'WWW-Authenticate': 'Bearer'},
        )

    # Validate the requested scopes
    granted_scopes = set(client.scopes if client.scopes else [])
    required_scopes = set(scope.split(' ') if scope else [])

    if not required_scopes.issubset(granted_scopes):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TokenErrorTypeEnum.missing_required_scopes.value,
            headers={'WWW-Authenticate': 'Bearer'},
        )

    # Return the client schema upon successful validation
    return client.id

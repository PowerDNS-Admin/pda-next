from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from models.api.auth import UserSchema, ClientSchema

oauth2_scheme_password = OAuth2PasswordBearer(tokenUrl='v1/token', auto_error=False)


async def validate_user_token_placeholder(token: str) -> UserSchema:
    pass


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    from app import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        yield session


async def get_principal(
        request: Request,
        session: AsyncSession = Depends(get_db_session),
        bearer_token: str = Depends(oauth2_scheme_password),
) -> UserSchema | ClientSchema:
    from loguru import logger
    from jose import JWTError, jwt
    from app import config
    from lib.security import ALGORITHM, COOKIE_NAME
    from models.db.auth import Session

    # Attempt OAuth Bearer Token Authentication
    if bearer_token:
        try:
            payload = jwt.decode(bearer_token, config.app.secret_key, algorithms=[ALGORITHM])
            logger.warning(payload)
        except JWTError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Invalid bearer token')
        user = await validate_user_token_placeholder(bearer_token)
        if user:
            return user

    # Attempt Session Token Authentication
    session_token = request.cookies.get(COOKIE_NAME)
    if session_token:
        db_session = await Session.get_by_token(session, session_token, request.client.host)
        if db_session:
            # Extend the session's expiration timestamp
            await Session.extend_session(session, db_session)
            return db_session.user

    # If neither works, raise an exception
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Not authenticated'
    )

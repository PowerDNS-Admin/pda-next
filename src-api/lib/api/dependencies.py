from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from models.api.auth import UserSchema, ClientSchema

oauth2_scheme_password = OAuth2PasswordBearer(tokenUrl='v1/token')


async def validate_user_token_placeholder(token: str) -> UserSchema:
    pass


async def validate_user_from_cookie(token: str) -> UserSchema:
    pass


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    from app import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        yield session


async def get_principal(request: Request, bearer_token: str = Depends(oauth2_scheme_password)) \
        -> UserSchema | ClientSchema:
    from loguru import logger
    from jose import JWTError, jwt
    from app import config
    from lib.security import ALGORITHM, COOKIE_NAME

    logger.warning(bearer_token)

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
    cookie_token = request.cookies.get(COOKIE_NAME)
    if cookie_token:
        user = await validate_user_from_cookie(cookie_token)
        if user:
            return user

    # If neither works, raise an exception
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Not authenticated'
    )

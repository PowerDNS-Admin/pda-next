from datetime import datetime, timedelta
from enum import Enum
from jose import jwt
from passlib.context import CryptContext

# TODO: Set the following constants from app settings
COOKIE_NAME = 'session_id'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class TokenGrantTypeEnum(str, Enum):
    """Defines the supported OAuth token grant types."""
    client_credentials = 'client_credentials'
    password = 'password'
    refresh_token = 'refresh_token'


def verify_hash(plain_value: str, hashed_value: str) -> bool:
    return crypt_context.verify(plain_value, hashed_value)


def hash_value(value: str) -> str:
    return crypt_context.hash(value)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    from datetime import timezone
    from app import config

    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, config.app.secret_key, algorithm=ALGORITHM)

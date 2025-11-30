from enum import Enum

from passlib.context import CryptContext

# TODO: Set the following constants from app settings
ACCESS_TOKEN_AGE = 3600
REFRESH_TOKEN_AGE = 1800
SESSION_AGE = 86400 # 1 day
SESSION_TOKEN_LENGTH = 128
COOKIE_NAME = 'session'
ALGORITHM = 'HS256'

crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class TokenGrantTypeEnum(str, Enum):
    """Defines the supported OAuth token grant types."""
    client_credentials = 'client_credentials'
    password = 'password'
    refresh_token = 'refresh_token'


class TokenErrorTypeEnum(str, Enum):
    """Defines the possible token grant error types."""
    invalid_client = 'invalid_client'
    invalid_user = 'invalid_user'
    invalid_token = 'invalid_token'
    unsupported_grant_type = 'unsupported_grant_type'
    missing_required_scopes = 'missing_required_scopes'


def verify_hash(plain_value: str, hashed_value: str) -> bool:
    return crypt_context.verify(plain_value, hashed_value)


def hash_value(value: str) -> str:
    return crypt_context.hash(value)

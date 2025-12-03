from enum import Enum

from passlib.context import CryptContext

ALGORITHM = 'HS256'
SESSION_TOKEN_LENGTH = 128
TENANT_HEADER_NAME = 'X-Tenant-Id'

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

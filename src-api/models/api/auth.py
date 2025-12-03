import uuid
from typing import Optional

from datetime import datetime
from pydantic import Field

from lib.permissions.definitions import Permissions
from models.api import BaseApiModel
from models.enums import PrincipalTypeEnum, UserStatusEnum


class Principal(BaseApiModel):
    """Represents an authentication principal."""

    id: Optional[uuid.UUID] = Field(
        title='User ID',
        description='The unique identifier of the principal.',
        default=None,
        examples=[uuid.uuid4()],
    )
    """The unique identifier of the principal."""

    type: PrincipalTypeEnum = Field(
        title='Type',
        description='The type of the principal.',
        examples=[
            PrincipalTypeEnum.client,
            PrincipalTypeEnum.user,
        ],
    )
    """The type of the principal."""

    permissions: Optional[set[str]] = Field(
        title='Principal Permissions',
        description='A list of permissions that the principal has.',
        default=None,
        examples=[
            Permissions.tenants_read,
            Permissions.zones_azone,
            Permissions.zones_rzone_read,
        ],
    )
    """The permissions that the principal has."""


class UserSchema(BaseApiModel):
    """Represents an authentication user for API interactions."""

    id: Optional[uuid.UUID] = Field(
        default=None,
        title='User ID',
        description='The unique identifier of the user.',
        examples=[uuid.uuid4()],
    )
    """The unique identifier of the user."""

    tenant_id: Optional[uuid.UUID] = Field(
        default=None,
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the user (if any).',
        examples=[uuid.uuid4()],
    )
    """The unique identifier of the tenant associated with the user (if any)."""

    username: str = Field(
        title='Username',
        description='The username of the user.',
        examples=['YourName', 'your.name@your-domain.com'],
    )
    """The username of the user."""

    status: UserStatusEnum = Field(
        default=UserStatusEnum.pending,
        title='Status',
        description='The status of the user.',
        examples=[
            UserStatusEnum.pending.value,
            UserStatusEnum.invited.value,
            UserStatusEnum.active.value,
            UserStatusEnum.suspended.value,
            UserStatusEnum.disabled.value,
        ],
    )
    """The status of the user."""

    created_at: Optional[datetime] = Field(
        default=datetime.now,
        title='Created At',
        description='The timestamp representing when the user was created.',
        examples=[datetime.now()],
    )
    """The timestamp representing when the user was created."""

    updated_at: Optional[datetime] = Field(
        default=datetime.now,
        title='Updated At',
        description='The timestamp representing when the user was last updated.',
        examples=[datetime.now()],
    )
    """The timestamp representing when the user was last updated."""

    authenticated_at: Optional[datetime] = Field(
        default=None,
        title='Authenticated At',
        description='The timestamp representing when the user was last authenticated.',
        examples=[datetime.now()],
    )
    """The timestamp representing when the user was last authenticated."""


class ClientSchema(BaseApiModel):
    """Represents an authentication client for API interactions."""
    id: Optional[uuid.UUID] = None
    tenant_id: Optional[uuid.UUID] = None
    user_id: Optional[uuid.UUID] = None
    name: str
    redirect_uri: Optional[str] = None
    scopes: Optional[list[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

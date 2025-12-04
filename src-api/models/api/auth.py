from typing import Optional
from uuid import UUID, uuid4

from datetime import datetime
from pydantic import Field

from lib.permissions.definitions import Permissions
from models.api import BaseApiModel
from models.enums import PrincipalTypeEnum, UserStatusEnum


class Principal(BaseApiModel):
    """Represents an authentication principal."""

    id: UUID = Field(
        title='Principal ID',
        description='The unique identifier of the principal.',
        examples=[uuid4()],
    )
    """The unique identifier of the principal."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the principal.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the principal."""
    
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
            Permissions.auth_users,
            Permissions.tenants_read,
            Permissions.zones_azone,
            Permissions.zones_rzone_read,
        ],
    )
    """The permissions that the principal has."""


class UserSchema(BaseApiModel):
    """Represents an authentication user for API interactions."""

    id: Optional[UUID] = Field(
        title='User ID',
        description='The unique identifier of the user.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the user."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the user (if any).',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the user (if any)."""

    username: str = Field(
        title='Username',
        description='The username of the user.',
        examples=['YourName', 'your.name@your-domain.com'],
    )
    """The username of the user."""

    status: UserStatusEnum = Field(
        title='Status',
        description='The status of the user.',
        default=UserStatusEnum.pending,
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
        title='Created At',
        description='The timestamp representing when the user was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the user was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the user was last updated.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the user was last updated."""

    authenticated_at: Optional[datetime] = Field(
        title='Authenticated At',
        description='The timestamp representing when the user was last authenticated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the user was last authenticated."""


class ClientSchema(BaseApiModel):
    """Represents an authentication client for API interactions."""
    id: Optional[UUID] = None
    tenant_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    name: str
    redirect_uri: Optional[str] = None
    scopes: Optional[list[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class UsersSchema(BaseApiModel):
    """Represents a list of authentication users for API interactions."""

    records: list[UserSchema] = Field(
        title='Users',
        description='A list of users found based on the current request criteria.',
        default_factory=list,
        # examples=[
        #     UserSchema(id=uuid4(), username='user1', status=UserStatusEnum.active),
        #     UserSchema(id=uuid4(), tenant_id=uuid4(), username='t1-user', status=UserStatusEnum.invited),
        #     UserSchema(id=uuid4(), tenant_id=uuid4(), username='t2-user', status=UserStatusEnum.disabled),
        # ],
    )
    """A list of users found based on the current request criteria."""

    total: int = Field(
        title='Total Users Found',
        description='The total number of users found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of users found based on the current request criteria."""

import uuid
from datetime import datetime
from pydantic import Field
from typing import Optional
from models.api import BaseApiModel
from models.enums import UserStatusEnum


class UserApi(BaseApiModel):
    """Represents an authentication user for API interactions."""

    id: Optional[uuid.UUID] = Field(
        default=None,
        title='User ID',
        description='The unique identifier of the user.',
        examples=[uuid.uuid4()],
        pattern='^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
    )
    """The unique identifier of the user."""

    tenant_id: Optional[uuid.UUID] = Field(
        default=None,
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the user (if any).',
        examples=[uuid.uuid4()],
        pattern='^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
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


class ClientApi(BaseApiModel):
    """Represents an authentication client for API interactions."""
    id: Optional[uuid.UUID] = None
    tenant_id: Optional[uuid.UUID] = None
    user_id: Optional[uuid.UUID] = None
    name: str
    redirect_uri: str
    scopes: list[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

from typing import Optional
from uuid import UUID, uuid4

from datetime import datetime
from pydantic import Field

from lib.permissions.definitions import Permissions, Permission
from models.api import BaseApiModel
from models.enums import PrincipalTypeEnum, UserStatusEnum, AuthenticatorTypeEnum


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

    permissions: Optional[set[Permission]] = Field(
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


class UserAuthenticatorSchema(BaseApiModel):
    """Represents an authentication user authenticator for API interactions."""

    id: Optional[UUID] = Field(
        title='Session ID',
        description='The unique identifier of the authenticator.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the session."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the authenticator (if any).',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the authenticator (if any)."""

    user_id: UUID = Field(
        title='User ID',
        description='The unique identifier of the user associated with the authenticator.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the user associated with the authenticator."""

    type: AuthenticatorTypeEnum = Field(
        title='Authenticator Type',
        description='The type of the authenticator.',
        examples=[
            AuthenticatorTypeEnum.WEBAUTHN,
            AuthenticatorTypeEnum.TOTP,
            AuthenticatorTypeEnum.SMS,
            AuthenticatorTypeEnum.EMAIL,
        ],
    )
    """The type of the authenticator."""

    name: str = Field(
        title='Authenticator Name',
        description='The name of the authenticator.',
        examples=[
            AuthenticatorTypeEnum.WEBAUTHN,
            AuthenticatorTypeEnum.TOTP,
            AuthenticatorTypeEnum.SMS,
            AuthenticatorTypeEnum.EMAIL,
        ],
    )
    """The name of the authenticator."""

    data: str = Field(
        title='Secret Data',
        description='The secret data of the authenticator.',
    )
    """The secret data of the authenticator."""

    enabled: bool = Field(
        title='Authenticator Enabled',
        description='Whether the authenticator is enabled.',
        default=True,
    )
    """Whether the authenticator is enabled."""

    created_at: Optional[datetime] = Field(
        title='Created At',
        description='The timestamp representing when the authenticator was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authenticator was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the authenticator was last updated.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authenticator was last updated."""

    used_at: Optional[datetime] = Field(
        title='Last Used At',
        description='The timestamp representing when the authenticator was last used.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authenticator was last used."""


class SessionSchema(BaseApiModel):
    """Represents an authentication session for API interactions."""

    id: Optional[UUID] = Field(
        title='Session ID',
        description='The unique identifier of the session.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the session."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the user (if any).',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the user (if any)."""

    user_id: UUID = Field(
        title='User ID',
        description='The unique identifier of the user associated with the session.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the user associated with the session."""

    remote_ip: str = Field(
        title='Client IP',
        description='The IPv4 or IPv6 address of the session client.',
        examples=['1.1.1.1', '2001:0db8:85a3:0000:0000:8a2e:0370:7334'],
    )
    """The IPv4 or IPv6 address of the session client."""

    token: str = Field(
        title='Session Token',
        description='The opaque identifier token for session persistence on clients.',
    )
    """The opaque identifier token for session persistence on clients."""

    data: Optional[dict] = Field(
        title='Session Data',
        description='The JSON-encoded data of the session.',
    )
    """The JSON-encoded data of the session."""

    created_at: Optional[datetime] = Field(
        title='Created At',
        description='The timestamp representing when the session was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the session was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the session was last updated.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the session was last updated."""

    expires_at: Optional[datetime] = Field(
        title='Expires At',
        description='The timestamp representing when the session expires.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the session expires."""


class ClientSchema(BaseApiModel):
    """Represents an authentication client for API interactions."""

    id: Optional[UUID] = Field(
        title='Client ID',
        description='The unique identifier of the client.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the client."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the client.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant that owns the client if any."""

    user_id: Optional[UUID] = Field(
        title='User ID',
        description='The unique identifier of the user associated with the client.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the user that owns the client if any."""

    name: str = Field(
        title='Client Name',
        description='The name of the client.',
        default=None,
    )
    """The name of the client."""

    redirect_uri: Optional[str] = Field(
        title='Redirect URI',
        description='The URL to redirect after authorization (if using auth code flow).',
        default=None,
        examples=['https://example.com'],
    )
    """The URL to redirect after authorization (if using auth code flow)."""

    scopes: Optional[list[Permission]] = Field(
        title='Scopes',
        description='The scopes associated with this client.',
        default=None,
        examples=[
            Permissions.auth_users,
            Permissions.auth_sessions,
            Permissions.auth_clients,
        ],
    )
    """A list of scopes associated with the client."""

    enabled: bool = Field(
        title='Client Status',
        description='Whether the client is enabled.',
        default=True,
    )
    """Whether the client is enabled."""

    created_at: Optional[datetime] = Field(
        title='Created At',
        description='The timestamp representing when the client was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the client was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the client was last updated.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the client was last updated."""

    expires_at: Optional[datetime] = Field(
        title='Expires At',
        description='The timestamp representing when the client expires.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the client expires."""


class UsersSchema(BaseApiModel):
    """Represents a list of authentication users for API interactions."""

    records: list[UserSchema] = Field(
        title='Users',
        description='A list of users found based on the current request criteria.',
        default_factory=list,
    )
    """A list of users found based on the current request criteria."""

    total: int = Field(
        title='Total Users Found',
        description='The total number of users found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of users found based on the current request criteria."""


class UserAuthenticatorsSchema(BaseApiModel):
    """Represents a list of authentication user authenticators for API interactions."""

    records: list[UserAuthenticatorSchema] = Field(
        title='Authenticators',
        description='A list of user authenticators found based on the current request criteria.',
        default_factory=list,
    )
    """A list of user authenticators found based on the current request criteria."""

    total: int = Field(
        title='Total User Authenticators Found',
        description='The total number of user authenticators found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of user authenticators found based on the current request criteria."""


class SessionsSchema(BaseApiModel):
    """Represents a list of authentication sessions for API interactions."""

    records: list[SessionSchema] = Field(
        title='Sessions',
        description='A list of sessions found based on the current request criteria.',
        default_factory=list,
    )
    """A list of sessions found based on the current request criteria."""

    total: int = Field(
        title='Total Sessions Found',
        description='The total number of sessions found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of sessions found based on the current request criteria."""


class ClientsSchema(BaseApiModel):
    """Represents a list of authentication client for API interactions."""

    records: list[ClientSchema] = Field(
        title='Clients',
        description='A list of client found based on the current request criteria.',
        default_factory=list,
    )
    """A list of client found based on the current request criteria."""

    total: int = Field(
        title='Total Clients Found',
        description='The total number of client found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of client found based on the current request criteria."""

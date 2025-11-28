"""
PDA Authentication Database Models

This file defines the database models associated with authentication functionality.
"""
import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Boolean, DateTime, String, TEXT, Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseSqlModel


class UserStatusEnum(str, Enum):
    """Defines the different statuses a user can have."""
    pending = 'pending'
    """Indicates a new user that has not yet been confirmed by an admin or had an invite sent."""

    invited = 'invited'
    """Indicates a new user that has had an invite sent but not yet confirmed by the admin or the user."""

    active = 'active'
    """Indicates a user that is active and fully confirmed."""

    suspended = 'suspended'
    """Indicates a user that is currently suspended."""

    disabled = 'disabled'
    """Indicates a user that is currently disabled."""


class AuthenticatorTypeEnum(str, Enum):
    """Defines the different authenticator types a user can have."""
    WEBAUTHN = 'WEBAUTHN'
    """A WebAuthn authenticator type."""

    TOTP = 'TOTP'
    """A time-based one-time password authenticator type."""

    SMS = 'SMS'
    """A SMS-based one-time password authenticator type."""

    EMAIL = 'EMAIL'
    """A email-based one-time password authenticator type."""


class User(BaseSqlModel):
    """Represents a user."""

    __tablename__ = 'pda_auth_users'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant that owns the record if any."""

    username: Mapped[str] = mapped_column(String, nullable=False)
    """The username of the user."""

    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    """The hashed password of the user."""

    status: Mapped[UserStatusEnum] = mapped_column(String, nullable=False, default=UserStatusEnum.pending)
    """The status of the user."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    authenticated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    """The timestamp representing when the user was last authenticated."""

    tenant = relationship('Tenant', back_populates='auth_users')
    """The tenant associated with the user."""

    authenticators = relationship('UserAuthenticator', back_populates='user')
    """A list of authenticators associated with the user."""

    sessions = relationship('Session', back_populates='user')
    """A list of auth sessions associated with the user."""

    clients = relationship('Client', back_populates='user')
    """A list of auth clients associated with the user."""

    access_tokens = relationship('AccessToken', back_populates='user')
    """A list of auth access tokens associated with the user."""

    refresh_tokens = relationship('RefreshToken', back_populates='user')
    """A list of auth refresh tokens associated with the user."""


class UserAuthenticator(BaseSqlModel):
    """Represents a user authenticator."""

    __tablename__ = 'pda_auth_user_authenticators'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant that owns the record if any."""

    user_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_auth_users.id'), nullable=False)
    """The unique identifier of the user that owns the record if any."""

    type_: Mapped[AuthenticatorTypeEnum] = mapped_column(String, nullable=False)
    """The type of the authenticator."""

    name: Mapped[str] = mapped_column(String, nullable=False)
    """The name of the authenticator."""

    data: Mapped[str] = mapped_column(TEXT, nullable=False)
    """The secret data of the authenticator."""

    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    """Whether the authenticator is enabled."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    used_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    """The timestamp representing when the authenticator was last used."""

    tenant = relationship('Tenant', back_populates='auth_user_authenticators')
    """The tenant associated with the user."""

    user = relationship('User', back_populates='authenticators')
    """A list of auth sessions associated with the user."""


class Session(BaseSqlModel):
    """Represents a user session."""

    __tablename__ = 'pda_auth_sessions'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant associated with the session if any."""

    user_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_auth_users.id'), nullable=False)
    """The unique identifier of the user associated with the session."""

    data: Mapped[str] = mapped_column(TEXT, nullable=False)
    """The JSON-encoded data of the session."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    """The timestamp representing when the session expires."""

    tenant = relationship('Tenant', back_populates='auth_sessions')
    """The tenant associated with the session."""

    user = relationship('User', back_populates='sessions')
    """The user associated with the session."""


class Client(BaseSqlModel):
    """Represents an authclient."""

    __tablename__ = 'pda_auth_clients'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant that owns the record if any."""

    user_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_auth_users.id'), nullable=True)
    """The unique identifier of the user that owns the record if any."""

    secret: Mapped[str] = mapped_column(String, nullable=False)
    """The authclient secret."""

    name: Mapped[str] = mapped_column(String, nullable=False)
    """The name of the client."""

    redirect_uri: Mapped[str] = mapped_column(String, nullable=False)
    """The URL to redirect after authorization (if using auth code flow)."""

    scopes: Mapped[str] = mapped_column(TEXT, nullable=True)
    """A JSON-encoded list of scopes associated with the client."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    """The timestamp representing when the client expires if ever."""

    tenant = relationship('Tenant', back_populates='auth_clients')
    """The tenant associated with the client."""

    user = relationship('User', back_populates='clients')
    """The user associated with the client."""

    access_tokens = relationship('AccessToken', back_populates='client')
    """A list of access tokens associated with the client."""

    refresh_tokens = relationship('RefreshToken', back_populates='client')
    """A list of refresh tokens associated with the client."""


class AccessToken(BaseSqlModel):
    """Represents an auth access token."""

    __tablename__ = 'pda_auth_access_tokens'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant that owns the record if any."""

    user_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_auth_users.id'), nullable=True)
    """The unique identifier of the user that owns the record if any."""

    client_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_auth_clients.id'), nullable=False)
    """The unique identifier of the authclient that owns the record."""

    token: Mapped[str] = mapped_column(String, nullable=False)
    """The auth access token."""

    scopes: Mapped[str] = mapped_column(TEXT, nullable=True)
    """A JSON-encoded list of scopes associated with the client."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    """The timestamp representing when the access token expires."""

    client = relationship('Client', back_populates='access_tokens')
    """The authclient associated with the access token."""

    tenant = relationship('Tenant', back_populates='auth_access_tokens')
    """The tenant associated with the access token."""

    user = relationship('User', back_populates='access_tokens')
    """The user associated with the access token."""


class RefreshToken(BaseSqlModel):
    """Represents an auth refresh token."""

    __tablename__ = 'pda_auth_refresh_tokens'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant that owns the record if any."""

    user_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_auth_users.id'), nullable=True)
    """The unique identifier of the user that owns the record if any."""

    client_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_auth_clients.id'), nullable=False)
    """The unique identifier of the authclient that owns the record."""

    token: Mapped[str] = mapped_column(String, nullable=False)
    """The auth refresh token."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    """The timestamp representing when the refresh token expires."""

    client = relationship('Client', back_populates='refresh_tokens')
    """The authclient associated with the refresh token."""

    tenant = relationship('Tenant', back_populates='auth_refresh_tokens')
    """The tenant associated with the refresh token."""

    user = relationship('User', back_populates='refresh_tokens')
    """The user associated with the refresh token."""

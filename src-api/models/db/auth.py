"""
PDA Authentication Database Models

This file defines the database models associated with authentication functionality.
"""
import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, TEXT, Uuid, text, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from uuid import UUID
from models.api.auth import UserSchema
from models.db import BaseSqlModel, JSONType
from models.enums import UserStatusEnum, AuthenticatorTypeEnum


class User(BaseSqlModel):
    """Represents a user."""

    __tablename__ = 'pda_auth_users'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant that owns the record if any."""

    username: Mapped[str] = mapped_column(String(100), nullable=False)
    """The username of the user."""

    hashed_password: Mapped[str] = mapped_column(TEXT, nullable=False)
    """The hashed password of the user."""

    status: Mapped[UserStatusEnum] = mapped_column(String(20), nullable=False, default=UserStatusEnum.pending)
    """The status of the user."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    authenticated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    """The timestamp representing when the user was last authenticated."""

    tenant = relationship('Tenant', back_populates='auth_users')
    """The tenant associated with the user."""

    authenticators = relationship('UserAuthenticator', back_populates='user')
    """A list of authenticators associated with the user."""

    sessions = relationship('Session', back_populates='user')
    """A list of auth sessions associated with the user."""

    clients = relationship('Client', back_populates='user')
    """A list of auth clients associated with the user."""

    refresh_tokens = relationship('RefreshToken', back_populates='user')
    """A list of auth refresh tokens associated with the user."""

    @property
    def password(self) -> str:
        """Returns the hashed user password."""
        return self.hashed_password

    @password.setter
    def password(self, value: str) -> None:
        """Sets the hashed user password from a non-hashed value."""
        from lib.security import hash_value
        self.hashed_password = hash_value(value)

    def verify_password(self, password: str) -> bool:
        """Verify if the given plain-text password matches the hashed password."""
        from lib.security import verify_hash
        return verify_hash(password, self.hashed_password)

    @staticmethod
    async def get_by_username(session: AsyncSession, username: str) -> 'User | None':
        """Retrieves a user object by its username."""
        from sqlalchemy import select
        stmt = select(User).where(User.username == username)
        return (await session.execute(stmt)).scalar_one_or_none()

    @staticmethod
    async def mark_authentication(session: AsyncSession, user: 'User') -> 'User':
        """Updates the given user's authenticated_at timestamp and returns the user."""
        from datetime import timezone

        user.authenticated_at = datetime.now(tz=timezone.utc)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user


class UserAuthenticator(BaseSqlModel):
    """Represents a user authenticator."""

    __tablename__ = 'pda_auth_user_authenticators'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant that owns the record if any."""

    user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_auth_users.id'), nullable=False)
    """The unique identifier of the user that owns the record if any."""

    type_: Mapped[AuthenticatorTypeEnum] = mapped_column(String(20), nullable=False)
    """The type of the authenticator."""

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    """The name of the authenticator."""

    data: Mapped[str] = mapped_column(TEXT, nullable=False)
    """The secret data of the authenticator."""

    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    """Whether the authenticator is enabled."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    used_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    """The timestamp representing when the authenticator was last used."""

    tenant = relationship('Tenant', back_populates='auth_user_authenticators')
    """The tenant associated with the user."""

    user = relationship('User', back_populates='authenticators')
    """A list of auth sessions associated with the user."""


class Session(BaseSqlModel):
    """Represents a user session."""

    __tablename__ = 'pda_auth_sessions'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant associated with the session if any."""

    user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_auth_users.id'), nullable=False)
    """The unique identifier of the user associated with the session."""

    remote_ip: Mapped[str] = mapped_column(String(45), nullable=False)
    """The IPv4 or IPv6 address of the session client."""

    token: Mapped[str] = mapped_column(TEXT, nullable=False)
    """The opaque identifier token for session persistence on clients."""

    data: Mapped[Optional[dict]] = mapped_column(JSONType, nullable=True)
    """The JSON-encoded data of the session."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    """The timestamp representing when the session expires."""

    tenant = relationship('Tenant', back_populates='auth_sessions')
    """The tenant associated with the session."""

    user = relationship('User', back_populates='sessions')
    """The user associated with the session."""

    @staticmethod
    async def get_by_id(session: AsyncSession, id: str | UUID) -> 'Session | None':
        """Retrieves a session object by its id."""
        from sqlalchemy import select
        if isinstance(id, str):
            id = UUID(id)
        stmt = select(Session).where(Session.id == id)
        return (await session.execute(stmt)).scalar_one_or_none()

    @staticmethod
    async def get_by_token(session: AsyncSession, token: str, remote_ip: Optional[str] = None) -> 'Session | None':
        """Retrieves a session object by its token and optionally remote ip."""
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
        stmt = select(Session).options(selectinload(Session.user)).where(Session.token == token)
        if isinstance(remote_ip, str):
            stmt.where(Session.remote_ip == remote_ip)
        return (await session.execute(stmt)).scalar_one_or_none()

    @staticmethod
    async def create_session(session: AsyncSession, user: UserSchema, remote_ip: Optional[str] = None) -> 'Session':
        """Creates an auth session and returns it."""
        import secrets
        from datetime import timedelta, timezone
        from lib.security import SESSION_AGE, SESSION_TOKEN_LENGTH

        expires_at = datetime.now(tz=timezone.utc) + timedelta(seconds=SESSION_AGE)

        db_session = Session(
            tenant_id=user.tenant_id,
            user_id=user.id,
            remote_ip=remote_ip,
            token=secrets.token_hex(SESSION_TOKEN_LENGTH),
            expires_at=expires_at,
            data=None,
        )

        session.add(db_session)
        await session.commit()
        await session.refresh(db_session)

        return db_session

    @staticmethod
    async def extend_session(session: AsyncSession, db_session: 'Session', total_seconds: Optional[int] = None) \
            -> 'Session':
        """Extends the expiration of a session."""
        from datetime import timedelta, timezone
        from lib.security import SESSION_AGE

        db_session.expires_at = datetime.now(tz=timezone.utc) + timedelta(seconds=total_seconds or SESSION_AGE)

        session.add(db_session)
        await session.commit()
        await session.refresh(db_session)

        return db_session

    @staticmethod
    async def destroy_session(session: AsyncSession, id: str | UUID) -> bool:
        """Destroys a session by id."""

        if isinstance(id, str):
            id = UUID(id)

        auth_session = await Session.get_by_id(session, id)

        if auth_session:
            await session.delete(auth_session)
            await session.commit()
            return True

        return False


class Client(BaseSqlModel):
    """Represents an authclient."""

    __tablename__ = 'pda_auth_clients'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant that owns the record if any."""

    user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_auth_users.id'), nullable=True)
    """The unique identifier of the user that owns the record if any."""

    hashed_secret: Mapped[str] = mapped_column(TEXT, nullable=False)
    """The hashed client secret."""

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    """The name of the client."""

    redirect_uri: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The URL to redirect after authorization (if using auth code flow)."""

    scopes: Mapped[Optional[list[str]]] = mapped_column(JSONType, nullable=True)
    """A JSON-encoded list of scopes associated with the client."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    """The timestamp representing when the client expires if ever."""

    tenant = relationship('Tenant', back_populates='auth_clients')
    """The tenant associated with the client."""

    user = relationship('User', back_populates='clients')
    """The user associated with the client."""

    refresh_tokens = relationship('RefreshToken', back_populates='client')
    """A list of refresh tokens associated with the client."""

    @property
    def secret(self) -> str:
        """Returns the hashed client secret."""
        return self.hashed_secret

    @secret.setter
    def secret(self, value: str) -> None:
        """Sets the hashed client secret from a non-hashed value."""
        from lib.security import hash_value
        self.hashed_secret = hash_value(value)

    def verify_secret(self, secret: str) -> bool:
        """Verify if the given plain-text client secret matches the hashed secret."""
        from lib.security import verify_hash
        return verify_hash(secret, self.hashed_secret)

    @staticmethod
    async def get_by_id(session: AsyncSession, id: str | Uuid) -> 'Client | None':
        """Retrieves a client object by its id."""
        from sqlalchemy import select
        if isinstance(id, str):
            id = UUID(id)
        stmt = select(Client).where(Client.id == id)
        return (await session.execute(stmt)).scalar_one_or_none()


class RefreshToken(BaseSqlModel):
    """Represents an auth refresh token."""

    __tablename__ = 'pda_auth_refresh_tokens'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant that owns the record if any."""

    user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_auth_users.id'), nullable=True)
    """The unique identifier of the user that owns the record if any."""

    client_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_auth_clients.id'), nullable=False)
    """The unique identifier of the authclient that owns the record."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    """The timestamp representing when the refresh token expires."""

    tenant = relationship('Tenant', back_populates='auth_refresh_tokens')
    """The tenant associated with the refresh token."""

    user = relationship('User', back_populates='refresh_tokens')
    """The user associated with the refresh token."""

    client = relationship('Client', back_populates='refresh_tokens')
    """The authclient associated with the refresh token."""

    def validate(self, client_id: str | UUID) -> bool:
        """Validates the refresh token matches the given client id and has not expired."""
        from datetime import timezone

        if isinstance(client_id, str):
            client_id = UUID(client_id)

        if client_id != self.client_id:
            return False

        if self.expires_at.replace(tzinfo=timezone.utc) < datetime.now(tz=timezone.utc):
            return False

        return True

    @staticmethod
    async def get_by_id(session: AsyncSession, id: str | UUID) -> 'RefreshToken | None':
        """Retrieves a refresh token object by its id."""
        from sqlalchemy import select
        if isinstance(id, str):
            id = UUID(id)
        stmt = select(RefreshToken).where(RefreshToken.id == id)
        return (await session.execute(stmt)).scalar_one_or_none()

    @staticmethod
    async def create_token(
            session: AsyncSession,
            expires_in: int,
            client_id: str | UUID,
            user_id: Optional[str | UUID | Mapped[UUID]] = None,
    ) -> 'RefreshToken':
        """Creates a refresh token for the given client and optionally user and returns the object."""
        from datetime import timedelta, timezone

        if isinstance(client_id, str):
            client_id = UUID(client_id)
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        expires_at = datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in)

        rt = RefreshToken(client_id=client_id, user_id=user_id, expires_at=expires_at)

        session.add(rt)
        await session.commit()
        await session.refresh(rt)
        return rt

    @staticmethod
    async def revoke_token(session: AsyncSession, rt: 'RefreshToken | str | UUID') -> None:
        """Revokes the given refresh token."""
        # Retrieve an ORM instance of the RefreshToken if a record ID was provided instance of an instance
        if isinstance(rt, str) or isinstance(rt, UUID):
            rt = RefreshToken.get_by_id(session, rt)
        elif not isinstance(rt, RefreshToken):
            raise TypeError('Invalid refresh token type')

        if not rt:
            raise ValueError('Invalid refresh token')

        await session.delete(rt)
        await session.commit()

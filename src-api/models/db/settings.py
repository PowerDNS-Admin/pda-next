"""
App Settings Database Models

This file defines the database models associated with app settings functionality.
"""
import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Boolean, DateTime, String, TEXT, Uuid, text, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db import BaseSqlModel


class SettingException(Exception):
    """A generic Setting related exception."""
    message: str = 'An unknown setting exception occurred.'
    """The exception's message."""

    key: Optional[str] = None
    """The key of the setting."""

    tenant_id: Optional[str | UUID] = None
    """The tenant id of the setting if any."""

    user_id: Optional[str | UUID] = None
    """The user id of the setting if any."""

    def __init__(
            self,
            message: str | None = None,
            key: Optional[str] = None,
            tenant_id: Optional[str | UUID] = None,
            user_id: Optional[str | UUID] = None,
    ):
        self.message = message
        self.key = key
        self.tenant_id = tenant_id
        self.user_id = user_id
        super().__init__(message)


class SettingExistsException(SettingException):
    """An exception raised when attempting to create a setting that already exists."""
    message: str = 'Setting already exists!'
    """The exception's message."""


class SettingMissingException(SettingException):
    """An exception raised when attempting to update a setting that does not exist."""
    message: str = 'Setting does not exist!'
    """The exception's message."""


class Setting(BaseSqlModel):
    """Represents an app setting."""

    __tablename__ = 'pda_settings'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant associated with the setting."""

    user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_auth_users.id'), nullable=True)
    """The unique identifier of the user associated with the setting."""

    key: Mapped[str] = mapped_column(String(255), nullable=False)
    """The key of the setting."""

    value: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The value of the setting."""

    default_value: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The default value of the setting."""

    overridable: Mapped[bool] = mapped_column(Boolean, nullable=True)
    """Whether the setting can be overridden in lower contexts."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the setting was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the setting was last updated."""

    tenant = relationship('Tenant', back_populates='settings')
    """The tenant associated with the setting."""

    user = relationship('User', back_populates='settings')
    """The user associated with the setting."""

    @staticmethod
    async def get_by_id(session: AsyncSession, id: str | UUID) -> 'Setting | None':
        """Retrieves a setting object by its id."""
        from sqlalchemy import select
        if isinstance(id, str):
            id = UUID(id)
        stmt = select(Setting).where(Setting.id == id)
        return (await session.execute(stmt)).scalar_one_or_none()

    @staticmethod
    async def get_by_criteria(
            session: AsyncSession,
            key: str,
            tenant_id: Optional[str | UUID] = None,
            user_id: Optional[str | UUID] = None,
            include_none: bool = False,
    ) -> 'Setting | None':
        """Retrieves a setting object by its key and optionally tenant and/or user id."""
        from sqlalchemy import select

        if isinstance(tenant_id, str):
            tenant_id = UUID(tenant_id)
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        stmt = select(Setting).where(Setting.key == key.value)

        if include_none or isinstance(tenant_id, UUID):
            stmt = stmt.where(Setting.tenant_id == tenant_id)

        if include_none or isinstance(user_id, UUID):
            stmt = stmt.where(Setting.user_id == user_id)

        return (await session.execute(stmt)).scalar_one_or_none()

    @staticmethod
    async def get_many(
            session: AsyncSession,
            key: Optional[str] = None,
            tenant_id: Optional[str | UUID] = None,
            user_id: Optional[str | UUID] = None,
    ) -> 'list[Setting]':
        """Retrieves multiple setting objects by based on the given attribute values."""
        from sqlalchemy import select

        if isinstance(tenant_id, str):
            tenant_id = UUID(tenant_id)
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        stmt = select(Setting).where(
            Setting.key == key.value, Setting.tenant_id == tenant_id, Setting.user_id == user_id
        )

        return list((await session.execute(stmt)).scalars().all())

    @staticmethod
    async def create_setting(
            session: AsyncSession,
            key: Optional[str],
            value: Optional[str] = None,
            default_value: Optional[str] = None,
            overridable: Optional[bool] = None,
            tenant_id: Optional[str | UUID] = None,
            user_id: Optional[str | UUID] = None,
    ) -> 'Setting':
        """
        Creates a single setting based on the given criteria and returns the created setting object.
        """

        setting = await Setting.get_by_criteria(session, key, tenant_id, user_id)

        # Validate that there isn't already an existing setting matching the given criteria
        if setting:
            raise SettingExistsException(
                f'The setting already exists: key: {key.value}, tenant_id: {tenant_id}, user_id: {user_id}',
                key=key,
                tenant_id=tenant_id,
                user_id=user_id,
            )

        # Validate tenant level override capability of setting if applicable
        if user_id and tenant_id:
            setting = await Setting.get_by_criteria(session, key, tenant_id)
            if setting and not setting.overridable:
                raise SettingExistsException(
                    f'The setting already exists at the tenant level and cannot be overridden: '
                    + f'key: {key.value}, tenant_id: {tenant_id}, user_id: {user_id}',
                    key=key,
                    tenant_id=tenant_id,
                    user_id=user_id,
                )

        # Validate system level override capability of setting if applicable
        if user_id or tenant_id:
            setting = await Setting.get_by_criteria(session, key, include_none=True)
            if setting and not setting.overridable:
                raise SettingExistsException(
                    f'The setting already exists at the system level and cannot be overridden: '
                    + f'key: {key.value}, tenant_id: {tenant_id}, user_id: {user_id}',
                    key=key,
                    tenant_id=tenant_id,
                    user_id=user_id,
                )

        setting = Setting(
            tenant_id=tenant_id,
            user_id=user_id,
            value=value,
            default_value=default_value,
            overridable=overridable,
        )

        session.add(setting)
        await session.commit()
        await session.refresh(setting)

        return setting

    @staticmethod
    async def update_setting(
            session: AsyncSession,
            key: Optional[str],
            value: Optional[str] = None,
            tenant_id: Optional[str | UUID] = None,
            user_id: Optional[str | UUID] = None,
    ) -> 'Setting':
        """Updates a single setting based on the given criteria and returns the updated setting object."""

        setting = await Setting.get_by_criteria(session, key, tenant_id, user_id)

        if not setting:
            raise SettingExistsException(
                f'The setting does not exist: key: {key.value}, tenant_id: {tenant_id}, user_id: {user_id}',
                key=key,
                tenant_id=tenant_id,
                user_id=user_id,
            )

        setting.value = value
        session.add(setting)
        await session.commit()
        await session.refresh(setting)

        return setting

    @staticmethod
    async def delete_setting(
            session: AsyncSession,
            key: Optional[str],
            tenant_id: Optional[str | UUID] = None,
            user_id: Optional[str | UUID] = None,
    ) -> None:
        """Deletes a single setting based on the given criteria and returns True if successful, False otherwise."""

        setting = await Setting.get_by_criteria(session, key, tenant_id, user_id, include_none=True)

        if not setting:
            raise SettingExistsException(
                f'The setting does not exist: key: {key.value}, tenant_id: {tenant_id}, user_id: {user_id}',
                key=key,
                tenant_id=tenant_id,
                user_id=user_id,
            )

        await session.delete(setting)
        await session.commit()

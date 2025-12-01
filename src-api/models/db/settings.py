"""
App Settings Database Models

This file defines the database models associated with app settings functionality.
"""
import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, String, TEXT, Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db import BaseSqlModel


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

    uri: Mapped[str] = mapped_column(String(255), nullable=False)
    """The uri of the setting."""

    key: Mapped[str] = mapped_column(String(255), nullable=False)
    """The key of the setting."""

    value: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The value of the setting."""

    overridable: Mapped[bool] = mapped_column(Boolean, nullable=True)
    """Whether the setting can be overridden in lower contexts."""

    readonly: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Whether the setting can be modified in non-system contexts."""

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

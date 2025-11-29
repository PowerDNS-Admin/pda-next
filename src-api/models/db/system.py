"""
PDA System Database Models

This file defines the database models associated with core system functionality.
"""
import uuid
from datetime import datetime
from sqlalchemy import DateTime, Integer, String, TEXT, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.db import BaseSqlModel


class StopgapDomain(BaseSqlModel):
    """Represents a stopgap domain."""

    __tablename__ = 'pda_stopgap_domains'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    """The friendly name of the stopgap domain."""

    fqdn: Mapped[str] = mapped_column(String(253), nullable=False)
    """The FQDN for the base stopgap domain."""

    restricted_hosts: Mapped[list[str]] = mapped_column(TEXT, nullable=True)
    """The list of hostnames that are restricted from use by tenants."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    tenants = relationship('Tenant', back_populates='stopgap_domain')
    """A list of tenants associated with the record."""


class RefTimezone(BaseSqlModel):
    """Represents an IANA timezone."""

    __tablename__ = 'pda_ref_timezones'
    """Defines the database table name."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    """The unique identifier of the record."""

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    """The unique IANA name for the timezone."""

    offset: Mapped[int] = mapped_column(Integer, nullable=False)
    """The offset from UTC in seconds for the timezone."""

    offset_dst: Mapped[int] = mapped_column(Integer, nullable=False)
    """The offset from UTC in seconds during daylight savings time for the timezone."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

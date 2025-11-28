"""
DNS Server Database Models

This file defines the database models associated with DNS server functionality.
"""
import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Boolean, DateTime, String, Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseSqlModel


class ServerTypeEnum(str, Enum):
    """Defines the different types of DNS servers there can be."""

    AUTHORITATIVE = "AUTHORITATIVE"
    """Represents the authoritative DNS server type."""

    RECURSIVE = "RECURSIVE"
    """Represents the recursive DNS server type."""

    PROXY = "PROXY"
    """Represents the load-balancing proxy DNS server type."""


class Server(BaseSqlModel):
    """Represents a DNS server."""

    __tablename__ = 'pda_servers'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=False)
    """The unique identifier of the tenant that owns the record."""

    type_: Mapped[ServerTypeEnum] = mapped_column(String, nullable=False)
    """The type of DNS server."""

    version: Mapped[str] = mapped_column(String, nullable=False)
    """The version of the server software."""

    hostname: Mapped[str] = mapped_column(String, nullable=False)
    """The hostname or IP address of the server."""

    api_url: Mapped[str] = mapped_column(String, nullable=False)
    """The fully qualified or relative URL of the server's API endpoint."""

    api_key: Mapped[str] = mapped_column(String, nullable=False)
    """The API key used to authenticate to the server API."""

    shared: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Indicates whether the server is shared between tenants."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    tenant = relationship('Tenant', back_populates='servers')
    """The tenant associated with the server."""

    auto_primaries = relationship('ServerAutoPrimary', back_populates='server')
    """A list of auto primary registrations associated with the server."""


class ServerAutoPrimary(BaseSqlModel):
    """Represents an autoprimary registration for a server."""

    __tablename__ = 'pda_server_auto_primaries'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=False)
    """The unique identifier of the tenant that owns the record."""

    server_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_servers.id'), nullable=False)
    """The unique identifier of the server this record belongs to."""

    ip: Mapped[str] = mapped_column(String, nullable=False)
    """The IP address of the autoprimary server."""

    nameserver: Mapped[str] = mapped_column(String, nullable=False)
    """The DNS name of the autoprimary server."""

    account: Mapped[str] = mapped_column(String, nullable=False)
    """The account name for the autoprimary server."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    tenant = relationship('Tenant', back_populates='auto_primaries')
    """The tenant associated with the auto primary registration."""

    server = relationship('Server', back_populates='auto_primaries')
    """The server associated with the auto primary registration."""

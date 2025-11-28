"""
DNS View Database Models

This file defines the database models associated with DNS view functionality.
"""
import uuid
from datetime import datetime
from sqlalchemy import DateTime, String, Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseSqlModel


class View(BaseSqlModel):
    """Represents a DNS zone view."""

    __tablename__ = 'pda_views'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=False)
    """The unique identifier of the tenant that owns the record."""

    name: Mapped[str] = mapped_column(String, nullable=False)
    """The name of the view."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    tenant = relationship('Tenant', back_populates='views')
    """The tenant associated with the view."""

    zones = relationship('ViewZone', back_populates='view')
    """A list of zones associated with the view."""

    networks = relationship('ViewNetwork', back_populates='view')
    """A list of networks associated with the view."""


class ViewZone(BaseSqlModel):
    """Represents a DNS zone associated with a view."""

    __tablename__ = 'pda_view_zones'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=False)
    """The unique identifier of the tenant that owns the record."""

    view_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_views.id'), nullable=False)
    """The unique identifier of the zone view this record belongs to."""

    fqdn: Mapped[str] = mapped_column(String, nullable=False)
    """The FQDN of the zone."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    tenant = relationship('Tenant', back_populates='view_zones')
    """The tenant associated with the view zone."""

    view = relationship('View', back_populates='zones')
    """The view associated with the zone."""


class ViewNetwork(BaseSqlModel):
    """Represents a zone view network assignment."""

    __tablename__ = 'pda_view_networks'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=False)
    """The unique identifier of the tenant that owns the record."""

    view_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_views.id'), nullable=False)
    """The unique identifier of the zone view this network assumes responsibility for."""

    network: Mapped[str] = mapped_column(String, nullable=False)
    """The CIDR specification of the network."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    tenant = relationship('Tenant', back_populates='view_networks')
    """The tenant associated with the view network."""

    view = relationship('View', back_populates='networks')
    """The view associated with the network."""

"""
PDA Tenant Database Models

This file defines the database models associated with tenant functionality.
"""
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import DateTime, String, Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.db import BaseSqlModel


class Tenant(BaseSqlModel):
    """Represents a tenant."""

    __tablename__ = 'pda_tenants'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the tenant."""

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    """The name of the tenant."""

    fqdn: Mapped[str] = mapped_column(String(253), nullable=True)
    """The FQDN for the tenant UI."""

    stopgap_domain_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_stopgap_domains.id'), nullable=True)
    """The unique identifier of the associated stopgap domain."""

    stopgap_hostname: Mapped[str] = mapped_column(String(253), nullable=True)
    """The hostname used within the associated stopgap domain."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the tenant was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the tenant was last updated."""

    stopgap_domain = relationship('StopgapDomain', back_populates='tenants', cascade='expunge, delete')
    """The stopgap domain associated with the tenant."""

    settings = relationship('Setting', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of settings associated with the tenant."""

    auth_users = relationship('User', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of auth users associated with the tenant."""

    auth_user_authenticators = relationship('UserAuthenticator', back_populates='tenant',
                                            cascade='all, delete, delete-orphan')
    """A list of auth user authenticators associated with the tenant."""

    auth_sessions = relationship('Session', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of auth sessions associated with the tenant."""

    auth_clients = relationship('Client', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of auth clients associated with the tenant."""

    auth_refresh_tokens = relationship('RefreshToken', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of auth refresh tokens associated with the tenant."""

    acl_roles = relationship('Role', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of ACL roles associated with the tenant."""

    acl_role_principals = relationship('RolePrincipal', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of ACL role principals associated with the tenant."""

    acl_policies = relationship('Policy', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of ACL policies associated with the tenant."""

    servers = relationship('Server', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of servers associated with the tenant."""

    auto_primaries = relationship('ServerAutoPrimary', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of server auto primary registrations associated with the tenant."""

    views = relationship('View', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of views associated with the tenant."""

    view_zones = relationship('ViewZone', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of view zones associated with the tenant."""

    view_networks = relationship('ViewNetwork', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of view networks associated with the tenant."""

    crypto_keys = relationship('CryptoKey', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of cryptographic keys associated with the tenant."""

    tsig_keys = relationship('TsigKey', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of TSIG keys associated with the tenant."""

    azones = relationship('AZone', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of authoritative zones associated with the tenant."""

    rzones = relationship('RZone', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of recursive zones associated with the tenant."""

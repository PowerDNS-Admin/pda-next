"""
DNS Keys Database Models

This file defines the database models associated with DNSSEC keys functionality.
"""
import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Integer, String, TEXT, Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db import BaseSqlModel, JSONType
from models.enums import CryptoKeyTypeEnum


class CryptoKey(BaseSqlModel):
    """Represents a DNSSEC cryptographic key."""

    __tablename__ = 'pda_crypto_keys'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the crypto key."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=False)
    """The unique identifier of the tenant that owns the crypto key."""

    internal_id: Mapped[int] = mapped_column(Integer, nullable=True)
    """The internal identifier, read only."""

    type_: Mapped[CryptoKeyTypeEnum] = mapped_column(String(20), nullable=False)
    """The type of the key."""

    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Whether the key is in active use."""

    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Whether the DNSKEY crypto key is published in the zone."""

    dns_key: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The DNSKEY crypto key for this key."""

    ds: Mapped[list[str]] = mapped_column(JSONType, nullable=True)
    """A list of DS crypto keys for this key."""

    cds: Mapped[list[str]] = mapped_column(JSONType, nullable=True)
    """A list of DS crypto keys for this key, filtered by CDS publication settings."""

    private_key: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The private key in ISC format."""

    algorithm: Mapped[str] = mapped_column(String(20), nullable=True)
    """The name of the algorithm of the key, should be a mnemonic."""

    bits: Mapped[int] = mapped_column(Integer, nullable=False)
    """The size of the key."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the crypto key was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the crypto key was last updated."""

    tenant = relationship('Tenant', back_populates='crypto_keys')
    """The tenant associated with the cryptographic key."""


class TsigKey(BaseSqlModel):
    """Represents a TSIG key."""

    __tablename__ = 'pda_tsig_keys'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the TSIG key."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=False)
    """The unique identifier of the tenant that owns the TSIG key."""

    internal_id: Mapped[str] = mapped_column(String(100), nullable=True)
    """The internal identifier, read only."""

    algorithm: Mapped[str] = mapped_column(String(20), nullable=True)
    """The algorithm of the TSIG key."""

    key: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The base64 encoded secret key."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the TSIG key was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the TSIG key was last updated."""

    tenant = relationship('Tenant', back_populates='tsig_keys')
    """The tenant associated with the TSIG key."""

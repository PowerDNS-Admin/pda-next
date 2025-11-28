"""
DNS Crypto Database Models

This file defines the database models associated with DNSSEC crypto functionality.
"""
import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Boolean, DateTime, Integer, String, Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseSqlModel


class CryptoKeyTypeEnum(str, Enum):
    """Defines the different types of DNSSEC cryptographic keys there can be."""

    KSK = "KSK"
    """DNSSEC Key Signing Key (KSK) type."""

    ZSK = "ZSK"
    """DNSSEC Zone Signing Key (ZSK) type."""

    CSK = "CSK"
    """DNSSEC Combined Signing Key (CSK) type."""


class CryptoKey(BaseSqlModel):
    """Represents a DNSSEC cryptographic key."""

    __tablename__ = 'pda_crypto_keys'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=False)
    """The unique identifier of the tenant that owns the record."""

    internal_id: Mapped[int] = mapped_column(Integer, nullable=True)
    """The internal identifier, read only."""

    type_: Mapped[CryptoKeyTypeEnum] = mapped_column(String, nullable=False)
    """The type of the key."""

    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Whether the key is in active use."""

    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Whether the DNSKEY record is published in the zone."""

    dns_key: Mapped[str] = mapped_column(String, nullable=True)
    """The DNSKEY record for this key."""

    ds: Mapped[list[str]] = mapped_column(String, nullable=True)
    """A list of DS records for this key."""

    cds: Mapped[list[str]] = mapped_column(String, nullable=True)
    """A list of DS records for this key, filtered by CDS publication settings."""

    private_key: Mapped[str] = mapped_column(String, nullable=True)
    """The private key in ISC format."""

    algorithm: Mapped[str] = mapped_column(String, nullable=True)
    """The name of the algorithm of the key, should be a mnemonic."""

    bits: Mapped[int] = mapped_column(Integer, nullable=False)
    """The size of the key."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    tenant = relationship('Tenant', back_populates='crypto_keys')
    """The tenant associated with the cryptographic key."""


class TsigKey(BaseSqlModel):
    """Represents a TSIG key."""

    __tablename__ = 'pda_tsig_keys'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=False)
    """The unique identifier of the tenant that owns the record."""

    internal_id: Mapped[str] = mapped_column(String, nullable=True)
    """The internal identifier, read only."""

    algorithm: Mapped[str] = mapped_column(String, nullable=True)
    """The algorithm of the TSIG key."""

    key: Mapped[str] = mapped_column(String, nullable=True)
    """The base64 encoded secret key."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    tenant = relationship('Tenant', back_populates='tsig_keys')
    """The tenant associated with the TSIG key."""

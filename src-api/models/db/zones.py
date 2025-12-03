"""
DNS Zone Database Models

This file defines the database models associated with DNS zone functionality.
"""
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Boolean, DateTime, Integer, String, TEXT, Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.db import BaseSqlModel, JSONType
from models.enums import AZoneKindEnum, RZoneKindEnum, ZoneRecordTypeEnum


class AZone(BaseSqlModel):
    """Represents an authoritative DNS zone."""

    __tablename__ = 'pda_azones'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the zone."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant that owns the zone if any."""

    fqdn: Mapped[str] = mapped_column(String(253), nullable=False)
    """The FQDN of the zone."""

    kind: Mapped[AZoneKindEnum] = mapped_column(String(20), nullable=False)
    """The kind of the zone."""

    serial: Mapped[int] = mapped_column(Integer, nullable=False)
    """The SOA serial number."""

    notified_serial: Mapped[int] = mapped_column(Integer, nullable=False)
    """The SOA serial notifications have been sent out for"""

    edited_serial: Mapped[int] = mapped_column(Integer, nullable=False)
    """The SOA serial as seen in query responses."""

    masters: Mapped[list[str]] = mapped_column(JSONType, nullable=True)
    """List of IP addresses configured as a master for this zone (“Slave” type zones only)."""

    dnssec: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Whether or not this zone is DNSSEC signed (inferred from presigned being true XOR presence of at least one cryptokey with active being true)."""

    nsec3param: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The NSEC3PARAM record."""

    nsec3narrow: Mapped[bool] = mapped_column(Boolean, nullable=True)
    """Whether or not the zone uses NSEC3 narrow."""

    presigned: Mapped[bool] = mapped_column(Boolean, nullable=True)
    """Whether or not the zone is pre-signed."""

    soa_edit: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The SOA-EDIT metadata item."""

    soa_edit_api: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The SOA-EDIT-API metadata item."""

    api_rectify: Mapped[bool] = mapped_column(Boolean, nullable=True)
    """Whether or not the zone will be rectified on data changes via the API."""

    zone: Mapped[str] = mapped_column(TEXT, nullable=True)
    """MAY contain a BIND-style zone file when creating a zone."""

    catalog: Mapped[str] = mapped_column(String(255), nullable=True)
    """The catalog this zone is a member of."""

    account: Mapped[str] = mapped_column(String(255), nullable=True)
    """MAY be set. Its value is defined by local policy."""

    master_tsig_key_ids: Mapped[list[str]] = mapped_column(JSONType, nullable=True)
    """The id of the TSIG keys used for master operation in this zone."""

    slave_tsig_key_ids: Mapped[list[str]] = mapped_column(JSONType, nullable=True)
    """The id of the TSIG keys used for slave operation in this zone."""

    shared: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Indicates whether the zone is shared between tenants."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the zone was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the zone was last updated."""

    tenant = relationship('Tenant', back_populates='azones')
    """The tenant associated with the zone."""

    records = relationship('AZoneRecord', back_populates='zone')
    """A list of resource records associated with the zone."""

    metadata_ = relationship('AZoneMetadata', back_populates='zone')
    """A list of metadata records associated with the zone."""


class AZoneRecord(BaseSqlModel):
    """Represents an authoritative DNS zone record."""

    __tablename__ = 'pda_azone_records'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant that owns the record if any."""

    zone_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_azones.id'), nullable=False)
    """The unique identifier of the zone this record belongs to."""

    name: Mapped[str] = mapped_column(String(255), nullable=True)
    """The name of the record."""

    type_: Mapped[ZoneRecordTypeEnum] = mapped_column(String(20), nullable=False)
    """The type of the record."""

    ttl: Mapped[int] = mapped_column(Integer, nullable=False)
    """DNS TTL of the record, in seconds."""

    content: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The content of the record."""

    comment: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The comment associated with the record."""

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Whether or not this record is disabled."""

    modified_at: Mapped[int] = mapped_column(Integer, nullable=True)
    """Timestamp of the last change to the record on the DNS server."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    zone = relationship('AZone', back_populates='records')
    """The zone associated with the resource record."""


class AZoneMetadata(BaseSqlModel):
    """Represents an authoritative DNS zone metadata record."""

    __tablename__ = 'pda_azone_metadata'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the metadata."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant that owns the metadata if any."""

    zone_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_azones.id'), nullable=False)
    """The unique identifier of the zone this metadata belongs to."""

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    """The kind of the metadata."""

    values: Mapped[list[str]] = mapped_column(TEXT, nullable=True)
    """The list of metadata values associated with this kind."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the metadata was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the metadata was last updated."""

    zone = relationship('AZone', back_populates='metadata_')
    """The zone associated with the metadata."""


class RZone(BaseSqlModel):
    """Represents a recursor DNS zone."""

    __tablename__ = 'pda_rzones'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the zone."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant that owns the zone if any."""

    fqdn: Mapped[str] = mapped_column(String(255), nullable=False)
    """The FQDN of the zone."""

    kind: Mapped[RZoneKindEnum] = mapped_column(String(20), nullable=False)
    """The kind of the zone."""

    servers: Mapped[list[str]] = mapped_column(Integer, nullable=False)
    """The list of upstream servers to forward queries to."""

    recursion_desired: Mapped[bool] = mapped_column(Boolean, nullable=True)
    """Whether or not the RD bit should be set in the upstream query for forwarded zone kinds."""

    notify_allowed: Mapped[bool] = mapped_column(Boolean, nullable=True)
    """Whether or not to permit incoming NOTIFY to wipe cache for the forwarded zone kind."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the zone was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the zone was last updated."""

    tenant = relationship('Tenant', back_populates='rzones')
    """The tenant associated with the zone."""

    records = relationship('RZoneRecord', back_populates='zone')
    """A list of resource records associated with the zone."""


class RZoneRecord(BaseSqlModel):
    """Represents a recursor DNS zone record."""

    __tablename__ = 'pda_rzone_records'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the resource record."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=True)
    """The unique identifier of the tenant that owns the resource record if any."""

    zone_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_rzones.id'), nullable=False)
    """The unique identifier of the zone this resource record belongs to."""

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    """The name of the record."""

    type_: Mapped[ZoneRecordTypeEnum] = mapped_column(String(20), nullable=False)
    """The type of the record."""

    ttl: Mapped[int] = mapped_column(Integer, nullable=False)
    """DNS TTL of the records, in seconds."""

    content: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The content of the record."""

    comment: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The comment associated with the record."""

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Whether or not this record is disabled."""

    modified_at: Mapped[int] = mapped_column(Integer, nullable=True)
    """Timestamp of the last change to the resource record on the DNS server."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the resource record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the resource record was last updated."""

    zone = relationship('RZone', back_populates='records')
    """The zone associated with the resource record."""

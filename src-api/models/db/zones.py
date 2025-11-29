"""
DNS Zone Database Models

This file defines the database models associated with DNS zone functionality.
"""
import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Boolean, DateTime, Integer, String, TEXT, Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import BaseSqlModel


class AZoneKindEnum(str, Enum):
    """Defines the different kinds of authoritative zones there can be."""
    NATIVE = "NATIVE"
    """A stand-alone zone that does not participate in DNS-based replication."""

    MASTER = "MASTER"
    """A source of truth for a zone's data."""

    SLAVE = "SLAVE"
    """A read-only replica of a zone obtained from a primary server."""

    PRODUCER = "PRODUCER"
    """A source of truth for a zone's data when using catalog zones."""

    CONSUMER = "CONSUMER"
    """A read-only replica of a zone obtained from a primary server when using catalog zones."""


class RZoneKindEnum(str, Enum):
    """Defines the different kinds of recursive zones there can be."""
    NATIVE = "Native"
    """A zone that a recursive DNS server acts authoritative for."""

    FORWARDED = "Forwarded"
    """A zone that a recursive DNS server forwards requests for."""


class ZoneRecordTypeEnum(str, Enum):
    """Defines the different types of zone records there can be."""
    A = "A"
    """The A record contains an IP address. It is stored as a decimal dotted quad string, for example: ‘203.0.113.210’."""

    AAAA = "AAAA"
    """The AAAA record contains an IPv6 address. An example: ‘2001:DB8:2000:bf0::1’."""

    AFSDB = "AFSDB"
    """A specialised record type for the ‘Andrew Filesystem’. Stored as: ‘#subtype hostname’, where subtype is a number."""

    APL = "APL"
    """The APL record, specified in RFC 3123, is used to specify a DNS RR type “APL” for address prefix lists."""

    CAA = "CAA"
    """The “Certification Authority Authorization” record, specified in RFC 6844, is used to specify Certificate Authorities that may issue certificates for a domain."""

    CERT = "CERT"
    """Specialised record type for storing certificates, defined in RFC 2538."""

    CDNSKEY = "CDNSKEY"
    """The CDNSKEY (Child DNSKEY) type is supported."""

    CDS = "CDS"
    """The CDS (Child DS) type is supported."""

    CNAME = "CNAME"
    """The ALIAS pseudo-record type is supported to provide CNAME-like mechanisms on a zone’s apex."""

    CSYNC = "CSYNC"
    """The CSYNC record is used for ‘Child-to-Parent Synchronization in DNS’, as described in RFC 7477."""

    DHCID = "DHCID"
    """A DNS Resource Record (RR) for Encoding Dynamic Host Configuration Protocol (DHCP) Information, as described in RFC 4701."""

    DLV = "DLV"
    """ The DNSSEC Lookaside Validation (DLV) DNS Resource Record, as described in RFC 4431."""

    DNSKEY = "DNSKEY"
    """The DNSKEY DNSSEC record type is fully supported, as described in RFC 4034."""

    DNAME = "DNAME"
    """The DNAME record, as specified in RFC 6672 is supported."""

    DS = "DS"
    """The DS DNSSEC record type is fully supported, as described in RFC 4034."""

    EUI48 = "EUI48"
    """Resource record for EUI-48 Address in the DNS, as described in RFC 7043."""

    EU164 = "EUI164"
    """Resource record for EUI-64 Address in the DNS, as described in RFC 7043."""

    HINFO = "HINFO"
    """Hardware Info record, used to specify CPU and operating system."""

    HTTPS = "HTTPS"
    """SVCB records, defined in (draft-ietf-dnsop-svcb-https-07) are used to facilitate the lookup of information needed to make connections to network services. The HTTPS RR is a variation of SVCB for HTTPS and HTTP origins."""

    IPSECKEY = "IPSECKEY"
    """A Method for Storing IPsec Keying Material in DNS, as described in RFC 4025."""

    KEY = "KEY"
    """The KEY record is fully supported. For its syntax, see RFC 2535."""

    KX = "KX"
    """ Key Exchange Delegation Record for the DNS, as described in RFC 2230."""

    L32 = "L32"
    """DNS Resource Records for the Identifier-Locator Network Protocol (ILNP), as described in RFC 6742."""

    L64 = "L64"
    """DNS Resource Records for the Identifier-Locator Network Protocol (ILNP), as described in RFC 6742."""

    LOC = "LOC"
    """The LOC record is fully supported. For its syntax, see RFC 1876."""

    LP = "LP"
    """DNS Resource Records for the Identifier-Locator Network Protocol (ILNP), as described in RFC 6742."""

    MINFO = "MINFO"
    """Mailbox or mail list information, as described in RFC 1035."""

    MR = "MR"
    """A mail rename domain name, as described in RFC 1035."""

    MX = "MX"
    """The MX record specifies a mail exchanger host for a domain."""

    NAPTR = "NAPTR"
    """Naming Authority Pointer, RFC 2915."""

    NID = "NID"
    """DNS Resource Records for the Identifier-Locator Network Protocol (ILNP), as described in RFC 6742."""

    NS = "NS"
    """Specifies nameservers for a domain."""

    NSEC = "NSEC"
    """The NSEC, NSEC3 and NSEC3PARAM DNSSEC record type are fully supported, as described in RFC 4034."""

    NSEC3 = "NSEC3"
    """The NSEC, NSEC3 and NSEC3PARAM DNSSEC record type are fully supported, as described in RFC 4034."""

    NSEC3PARAM = "NSEC3PARAM"
    """The NSEC, NSEC3 and NSEC3PARAM DNSSEC record type are fully supported, as described in RFC 4034."""

    OPENPGPKEY = "OPENPGPKEY"
    """The OPENPGPKEY records, specified in RFC 7929, are used to bind OpenPGP certificates to email addresses."""

    PTR = "PTR"
    """Reverse pointer, used to specify the host name belonging to an IP or IPv6 address."""

    RKEY = "RKEY"
    """The resource record for storing keys which encrypt NAPTR records."""

    RP = "RP"
    """Responsible Person record, as described in RFC 1183."""

    RRSIG = "RRSIG"
    """The RRSIG DNSSEC record type is fully supported, as described in RFC 4034."""

    SMIMEA = "SMIMEA"
    """The SMIMEA record type, specified in RFC 8162, is used to bind S/MIME certificates to domains."""

    SOA = "SOA"
    """The SOA record type specifies the name of the primary nameserver (‘the primary’), the hostmaster and a set of numbers indicating how the data in this domain expires and how often it needs to be checked."""

    SPF = "SPF"
    """SPF records can be used to store Sender Policy Framework details (RFC 4408)."""

    SSHFP = "SSHFP"
    """The SSHFP record type, used for storing Secure Shell (SSH) fingerprints, is fully supported, as described in RFC 4255."""

    SRV = "SRV"
    """SRV records can be used to encode the location and port of services on a domain name."""

    SVCB = "SVCB"
    """SVCB records, defined in (draft-ietf-dnsop-svcb-https-07) are used to facilitate the lookup of information needed to make connections to network services."""

    TKEY = "TKEY"
    """The TKEY (RFC 2930) and TSIG records (RFC 2845), used for key-exchange and authenticated AXFRs, are supported."""

    TSIG = "TSIG"
    """The TKEY (RFC 2930) and TSIG records (RFC 2845), used for key-exchange and authenticated AXFRs, are supported."""

    TLSA = "TLSA"
    """The TLSA records, specified in RFC 6698, are used to bind SSL/TLS certificate to named hosts and ports."""

    TXT = "TXT"
    """The TXT field can be used to attach textual data to a domain."""

    URI = "URI"
    """The URI record, specified in RFC 7553, is used to publish mappings from hostnames to URIs."""

    ZONEMD = "ZONEMD"
    """The ZONEMD record, specified in RFC 8976, is used to validate zones."""

    UNKNOWN = "UNKNOWN"
    """PowerDNS supports (RFC 3597) syntax for serving unknown record types."""


class AZone(BaseSqlModel):
    """Represents an authoritative DNS zone."""

    __tablename__ = 'pda_azones'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=False)
    """The unique identifier of the tenant that owns the record."""

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

    masters: Mapped[list[str]] = mapped_column(TEXT, nullable=True)
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

    master_tsig_key_ids: Mapped[list[str]] = mapped_column(TEXT, nullable=True)
    """The id of the TSIG keys used for master operation in this zone."""

    slave_tsig_key_ids: Mapped[list[str]] = mapped_column(TEXT, nullable=True)
    """The id of the TSIG keys used for slave operation in this zone."""

    shared: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Indicates whether the zone is shared between tenants."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

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

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=False)
    """The unique identifier of the tenant that owns the record."""

    zone_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_azones.id'), nullable=False)
    """The unique identifier of the zone this record belongs to."""

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

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=False)
    """The unique identifier of the tenant that owns the record."""

    zone_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_azones.id'), nullable=False)
    """The unique identifier of the zone this record belongs to."""

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    """The kind of the metadata."""

    values: Mapped[list[str]] = mapped_column(TEXT, nullable=True)
    """The list of metadata values associated with this kind."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    zone = relationship('AZone', back_populates='metadata_')
    """The zone associated with the metadata record."""


class RZone(BaseSqlModel):
    """Represents a recursor DNS zone."""

    __tablename__ = 'pda_rzones'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=False)
    """The unique identifier of the tenant that owns the record."""

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
    """The timestamp representing when the record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    tenant = relationship('Tenant', back_populates='rzones')
    """The tenant associated with the zone."""

    records = relationship('RZoneRecord', back_populates='zone')
    """A list of resource records associated with the zone."""


class RZoneRecord(BaseSqlModel):
    """Represents a recursor DNS zone record."""

    __tablename__ = 'pda_rzone_records'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_tenants.id'), nullable=False)
    """The unique identifier of the tenant that owns the record."""

    zone_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_rzones.id'), nullable=False)
    """The unique identifier of the zone this record belongs to."""

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

    zone = relationship('RZone', back_populates='records')
    """The zone associated with the resource record."""

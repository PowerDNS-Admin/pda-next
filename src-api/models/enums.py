from enum import Enum


class UserStatusEnum(str, Enum):
    """Defines the different statuses a user can have."""
    pending = 'pending'
    """Indicates a new user that has not yet been confirmed by an admin or had an invite sent."""

    invited = 'invited'
    """Indicates a new user that has had an invite sent but not yet confirmed by the admin or the user."""

    active = 'active'
    """Indicates a user that is active and fully confirmed."""

    suspended = 'suspended'
    """Indicates a user that is currently suspended."""

    disabled = 'disabled'
    """Indicates a user that is currently disabled."""


class AuthenticatorTypeEnum(str, Enum):
    """Defines the different authenticator types a user can have."""
    WEBAUTHN = 'WEBAUTHN'
    """A WebAuthn authenticator type."""

    TOTP = 'TOTP'
    """A time-based one-time password authenticator type."""

    SMS = 'SMS'
    """A SMS-based one-time password authenticator type."""

    EMAIL = 'EMAIL'
    """A email-based one-time password authenticator type."""


class ResourceTypeEnum(Enum):
    """Defines the resource types of PDA."""
    auth_user = 'auth_user'
    auth_user_authenticator = 'auth_user_authenticator'
    auth_session = 'auth_session'
    auth_client = 'auth_client'
    auth_access_token = 'auth_access_token'
    auth_refresh_token = 'auth_refresh_token'
    acl = 'acl'
    acl_role = 'acl_role'
    acl_role_permission = 'acl_role_permission'
    system_ref_timezone = 'system_ref_timezone'
    system_stopgap_domain = 'system_stopgap_domain'
    task_job = 'task_job'
    task_job_activity = 'task_job_activity'
    tenant = 'tenant'
    server = 'server'
    server_auto_primary = 'server_auto_primary'
    view = 'view'
    view_zone = 'view_zone'
    view_network = 'view_network'
    key_crypto_key = 'key_crypto_key'
    key_tsig_key = 'key_tsig_key'
    zone_azone = 'zone_azone'
    zone_azone_record = 'zone_azone_record'
    zone_azone_metadata = 'zone_azone_metadata'
    zone_rzone = 'zone_rzone'
    zone_rzone_record = 'zone_rzone_record'


class PrincipalTypeEnum(Enum):
    """Defines the principal types of PDA."""
    user = 'user'
    role = 'role'
    tenant = 'tenant'


class PermissionEnum(str, Enum):
    """Defines the permissions of PDA."""
    auth_all = 'auth:*'
    auth_user_all = 'auth:user:*'
    auth_user_list = 'auth:user:list'
    auth_user_create = 'auth:user:create'
    auth_user_read = 'auth:user:read'
    auth_user_update = 'auth:user:update'
    auth_user_delete = 'auth:user:delete'

    acl_all = 'acl:*'
    acl_role_all = 'acl:role:*'
    acl_role_list = 'acl:role:list'
    acl_role_create = 'acl:role:create'
    acl_role_read = 'acl:role:read'
    acl_role_update = 'acl:role:update'
    acl_role_delete = 'acl:role:delete'

    audit_all = 'audit:*'
    audit_read = 'audit:read'
    audit_export = 'audit:export'

    system_all = 'system:*'
    system_stopgap_domain_all = 'system:stopgap_domain:*'
    system_stopgap_domain_list = 'system:stopgap_domain:list'
    system_stopgap_domain_create = 'system:stopgap_domain:create'
    system_stopgap_domain_read = 'system:stopgap_domain:read'
    system_stopgap_domain_update = 'system:stopgap_domain:update'
    system_stopgap_domain_delete = 'system:stopgap_domain:delete'
    system_ref_timezone_all = 'system:ref_timezone:*'
    system_ref_timezone_list = 'system:ref_timezone:list'
    system_ref_timezone_create = 'system:ref_timezone:create'
    system_ref_timezone_read = 'system:ref_timezone:read'
    system_ref_timezone_update = 'system:ref_timezone:update'
    system_ref_timezone_delete = 'system:ref_timezone:delete'

    task_all = 'task:*'
    task_job_all = 'task:job:*'
    task_job_list = 'task:job:list'
    task_job_create = 'task:job:create'
    task_job_read = 'task:job:read'
    task_job_update = 'task:job:update'
    task_job_delete = 'task:job:delete'

    tenant_all = 'tenant:*'
    tenant_list = 'tenant:list'
    tenant_create = 'tenant:create'
    tenant_read = 'tenant:read'
    tenant_update = 'tenant:update'
    tenant_delete = 'tenant:delete'

    server_all = 'server:*'
    server_list = 'server:list'
    server_create = 'server:create'
    server_read = 'server:read'
    server_update = 'server:update'
    server_delete = 'server:delete'

    view_all = 'view:*'
    view_list = 'view:list'
    view_create = 'view:create'
    view_read = 'view:read'
    view_update = 'view:update'
    view_delete = 'view:delete'

    key_all = 'key:*'
    key_list = 'key:list'
    key_create = 'key:create'
    key_read = 'key:read'
    key_update = 'key:update'
    key_delete = 'key:delete'
    key_crypto_all = 'key:crypto:*'
    key_crypto_list = 'key:crypto:list'
    key_crypto_create = 'key:crypto:create'
    key_crypto_read = 'key:crypto:read'
    key_crypto_update = 'key:crypto:update'
    key_crypto_delete = 'key:crypto:delete'
    key_tsig_all = 'key:tsig:*'
    key_tsig_list = 'key:tsig:list'
    key_tsig_create = 'key:tsig:create'
    key_tsig_read = 'key:tsig:read'
    key_tsig_update = 'key:tsig:update'
    key_tsig_delete = 'key:tsig:delete'

    zone_all = 'zone:*'
    zone_list = 'zone:list'
    zone_create = 'zone:create'
    zone_read = 'zone:read'
    zone_update_any = 'zone:update:any'
    zone_update_own = 'zone:update:own'
    zone_delete_any = 'zone:delete:any'
    zone_delete_own = 'zone:delete:own'
    zone_share = 'zone:share'

    record_all = 'record:*'
    record_list = 'record:list'
    record_create = 'record:create'
    record_read = 'record:read'
    record_update_any = 'record:update:any'
    record_update_own = 'record:update:own'
    record_delete_any = 'record:delete:any'
    record_delete_own = 'record:delete:own'
    record_claim = 'record:claim'


class CryptoKeyTypeEnum(str, Enum):
    """Defines the different types of DNSSEC cryptographic keys there can be."""

    KSK = "KSK"
    """DNSSEC Key Signing Key (KSK) type."""

    ZSK = "ZSK"
    """DNSSEC Zone Signing Key (ZSK) type."""

    CSK = "CSK"
    """DNSSEC Combined Signing Key (CSK) type."""


class ServerTypeEnum(str, Enum):
    """Defines the different types of DNS servers there can be."""

    AUTHORITATIVE = "AUTHORITATIVE"
    """Represents the authoritative DNS server type."""

    RECURSIVE = "RECURSIVE"
    """Represents the recursive DNS server type."""

    PROXY = "PROXY"
    """Represents the load-balancing proxy DNS server type."""


class TaskJobStatusEnum(str, Enum):
    """Defines the different task job statuses."""
    received = "received"
    """When a task job has been received but not yet started."""

    revoked = "revoked"
    """When a task job has been revoked before completion."""

    running = "running"
    """When a task job is actively running."""

    retry = "retry"
    """When a task job has failed to complete successfully and is awaiting another attempt."""

    success = "success"
    """When a task job has completed successfully."""

    failed = "failed"
    """When a task job has failed permanently having exhausted any available retry attempts."""

    internal_error = "internal_error"
    """When a task job has failed permanently from having an internal error."""


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

from typing import Optional

from pydantic import BaseModel, Field

from models.enums import ResourceTypeEnum, PrincipalTypeEnum


class classproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, owner):
        # Call the decorated function with the class object (owner)
        return self.func(owner)


class Permission(BaseModel):
    """Provides an interface for defining a system permission and applying it accordingly."""

    uri: str = Field(
        title='Permission URI',
        description='The uniform resource identifier (URI) used in policy definition and assignment storage to represent the permission.',
        pattern=r'^[a-z]+(?:[:][a-z0-9_]+)?(?:[:][a-z0-9_]+)?(?:[:][a-z0-9_]+)?$',
    )
    """The uniform resource identifier (URI) used in policy definition and assignment storage to represent the permission."""

    title: str = Field(
        title='Permission Title',
        description='The friendly title of the permission.',
    )
    """The friendly title of the permission."""

    description: str = Field(
        title='Permission Description',
        description='The description of the permission.',
    )
    """The description of the permission."""

    principal_types: Optional[list[PrincipalTypeEnum]] = Field(
        title='Applicable Principal Types',
        description='A list of principal types this permission can be applied to.',
        default=None,
    )
    """A list of principal types this permission can be applied to."""

    resource_types: Optional[list[ResourceTypeEnum]] = Field(
        title='Applicable Resource Types',
        description='A list of resource types this permission can be applied to.',
        default=None,
    )
    """A list of resource types this permission can be applied to."""


class Permissions:
    """Defines the available permissions of the system."""

    @classproperty
    def scopes(cls) -> dict[str, str]:
        """Provides a dictionary of available permissions in the form of OAuth API scopes."""
        return {p.uri: p.title for k, p in cls.__dict__.items() if not k.startswith('__') and k != 'scopes'}

    auth_users: Permission = Permission(
        uri="auth:users",
        title="All Users Permissions",
        description="Includes all users-related permissions.",
        resource_types=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_user_authenticator,
        ],
    )
    """Includes all users-related permissions."""

    auth_users_read: Permission = Permission(
        uri="auth:users:read",
        title="Read Users",
        description="Provides the ability to read user records within context.",
        resource_types=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_user_authenticator,
        ],
    )
    """Provides the ability to read user records within context."""

    auth_users_create: Permission = Permission(
        uri="auth:users:create",
        title="Create Users",
        description="Provides the ability to create user records within context.",
        resource_types=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_user_authenticator,
        ],
    )
    """Provides the ability to create user records within context."""

    auth_users_update: Permission = Permission(
        uri="auth:users:update",
        title="Update Users",
        description="Provides the ability to update user records within context.",
        resource_types=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_user_authenticator,
        ],
    )
    """Provides the ability to update user records within context."""

    auth_users_delete: Permission = Permission(
        uri="auth:users:delete",
        title="Delete Users",
        description="Provides the ability to delete user records within context.",
        resource_types=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_user_authenticator,
        ],
    )
    """Provides the ability to delete user records within context."""

    auth_users_reset_password: Permission = Permission(
        uri="auth:users:reset_password",
        title="Reset User Passwords",
        description="Provides the ability to reset user passwords within context.",
        resource_types=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_user_authenticator,
        ],
    )
    """Provides the ability to reset user passwords within context."""

    auth_users_change_status: Permission = Permission(
        uri="auth:users:change_status",
        title="Change User Statuses",
        description="Provides the ability to change a user's status within context.",
        resource_types=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_user_authenticator,
        ],
    )
    """Provides the ability to change a user's status within context."""

    auth_sessions: Permission = Permission(
        uri="auth:sessions",
        title="All Sessions Permissions",
        description="Includes all sessions-related permissions.",
        resource_types=[
            ResourceTypeEnum.auth_session,
        ],
    )
    """Includes all sessions-related permissions."""

    auth_sessions_read: Permission = Permission(
        uri="auth:sessions:read",
        title="Read Sessions",
        description="Provides the ability to read session records within context.",
        resource_types=[
            ResourceTypeEnum.auth_session,
        ],
    )
    """Provides the ability to read session records within context."""

    auth_sessions_delete: Permission = Permission(
        uri="auth:sessions:delete",
        title="Delete Sessions",
        description="Provides the ability to delete session records within context.",
        resource_types=[
            ResourceTypeEnum.auth_session,
        ],
    )
    """Provides the ability to delete session records within context."""

    auth_clients: Permission = Permission(
        uri="auth:clients",
        title="All Client Permissions",
        description="Includes all clients-related permissions.",
        resource_types=[
            ResourceTypeEnum.auth_client,
        ],
    )
    """Includes all clients-related permissions."""

    auth_clients_read: Permission = Permission(
        uri="auth:clients:read",
        title="Read Clients",
        description="Provides the ability to read client records within context.",
        resource_types=[
            ResourceTypeEnum.auth_client,
        ],
    )
    """Provides the ability to read client records within context."""

    auth_clients_create: Permission = Permission(
        uri="auth:clients:create",
        title="Create Clients",
        description="Provides the ability to create client records within context.",
        resource_types=[
            ResourceTypeEnum.auth_client,
        ],
    )
    """Provides the ability to create client records within context."""

    auth_clients_update: Permission = Permission(
        uri="auth:clients:update",
        title="Update Clients",
        description="Provides the ability to update client records within context.",
        resource_types=[
            ResourceTypeEnum.auth_client,
        ],
    )
    """Provides the ability to update client records within context."""

    auth_clients_delete: Permission = Permission(
        uri="auth:clients:delete",
        title="Delete Clients",
        description="Provides the ability to delete client records within context.",
        resource_types=[
            ResourceTypeEnum.auth_client,
        ],
    )
    """Provides the ability to delete client records within context."""
    
    acl_roles: Permission = Permission(
        uri="acl:roles",
        title="All Roles Permissions",
        description="Includes all roles-related permissions.",
        resource_types=[
            ResourceTypeEnum.acl_role,
            ResourceTypeEnum.acl_role_permission,
        ],
    )
    """Includes all roles-related permissions."""

    acl_roles_read: Permission = Permission(
        uri="acl:roles:read",
        title="Read Roles",
        description="Provides the ability to read role records within context.",
        resource_types=[
            ResourceTypeEnum.acl_role,
            ResourceTypeEnum.acl_role_permission,
        ],
    )
    """Provides the ability to read role records within context."""

    acl_roles_create: Permission = Permission(
        uri="acl:roles:create",
        title="Create Roles",
        description="Provides the ability to create role records within context.",
        resource_types=[
            ResourceTypeEnum.acl_role,
            ResourceTypeEnum.acl_role_permission,
        ],
    )
    """Provides the ability to create role records within context."""

    acl_roles_update: Permission = Permission(
        uri="acl:roles:update",
        title="Update Roles",
        description="Provides the ability to update role records within context.",
        resource_types=[
            ResourceTypeEnum.acl_role,
            ResourceTypeEnum.acl_role_permission,
        ],
    )
    """Provides the ability to update role records within context."""

    acl_roles_delete: Permission = Permission(
        uri="acl:roles:delete",
        title="Delete Roles",
        description="Provides the ability to delete role records within context.",
        resource_types=[
            ResourceTypeEnum.acl_role,
            ResourceTypeEnum.acl_role_permission,
        ],
    )
    """Provides the ability to delete role records within context."""

    acl_policies: Permission = Permission(
        uri="acl:policies",
        title="All Policies Permissions",
        description="Includes all policies-related permissions.",
        resource_types=[
            ResourceTypeEnum.acl_policy,
        ],
    )
    """Includes all policies-related permissions."""

    acl_policies_read: Permission = Permission(
        uri="acl:policies:read",
        title="Read Policies",
        description="Provides the ability to read policy records within context.",
        resource_types=[
            ResourceTypeEnum.acl_policy,
        ],
    )
    """Provides the ability to read policy records within context."""

    acl_policies_create: Permission = Permission(
        uri="acl:policies:create",
        title="Create Policies",
        description="Provides the ability to create policy records within context.",
        resource_types=[
            ResourceTypeEnum.acl_policy,
        ],
    )
    """Provides the ability to create policy records within context."""

    acl_policies_update: Permission = Permission(
        uri="acl:policies:update",
        title="Update Policies",
        description="Provides the ability to update policy records within context.",
        resource_types=[
            ResourceTypeEnum.acl_policy,
        ],
    )
    """Provides the ability to update policy records within context."""

    acl_policies_delete: Permission = Permission(
        uri="acl:policies:delete",
        title="Delete Policies",
        description="Provides the ability to delete policy records within context.",
        resource_types=[
            ResourceTypeEnum.acl_policy,
        ],
    )
    """Provides the ability to delete policy records within context."""

    settings: Permission = Permission(
        uri="settings:setting",
        title="All Settings Permissions",
        description="Includes all settings-related permissions.",
        resource_types=[
            ResourceTypeEnum.settings_setting,
        ],
    )
    """Includes all settings-related permissions."""

    settings_read: Permission = Permission(
        uri="settings:setting:read",
        title="Read Settings",
        description="Provides the ability to read settings records within context.",
        resource_types=[
            ResourceTypeEnum.settings_setting,
        ],
    )
    """Provides the ability to read settings records within context."""

    settings_create: Permission = Permission(
        uri="settings:setting:create",
        title="Create Settings",
        description="Provides the ability to create settings records within context.",
        resource_types=[
            ResourceTypeEnum.settings_setting,
        ],
    )
    """Provides the ability to create settings records within context."""

    settings_update: Permission = Permission(
        uri="settings:setting:update",
        title="Update Settings",
        description="Provides the ability to update settings records within context.",
        resource_types=[
            ResourceTypeEnum.settings_setting,
        ],
    )
    """Provides the ability to update settings records within context."""

    settings_delete: Permission = Permission(
        uri="settings:setting:delete",
        title="Delete Settings",
        description="Provides the ability to delete settings records within context.",
        resource_types=[
            ResourceTypeEnum.settings_setting,
        ],
    )
    """Provides the ability to delete settings records within context."""

    system_stopgap_domains: Permission = Permission(
        uri="system:stopgap_domains",
        title="All Stopgap Domains Permissions",
        description="Includes all stopgap domains-related permissions.",
        resource_types=[
            ResourceTypeEnum.system_stopgap_domain,
        ],
    )
    """Includes all stopgap domains-related permissions."""

    system_stopgap_domains_read: Permission = Permission(
        uri="system:stopgap_domains:read",
        title="Read Stopgap Domains",
        description="Provides the ability to read stopgap domains records within context.",
        resource_types=[
            ResourceTypeEnum.system_stopgap_domain,
        ],
    )
    """Provides the ability to read stopgap domains records within context."""

    system_stopgap_domains_create: Permission = Permission(
        uri="system:stopgap_domains:create",
        title="Create Stopgap Domains",
        description="Provides the ability to create stopgap domains records within context.",
        resource_types=[
            ResourceTypeEnum.system_stopgap_domain,
        ],
    )
    """Provides the ability to create stopgap domains records within context."""

    system_stopgap_domains_update: Permission = Permission(
        uri="system:stopgap_domains:update",
        title="Update Stopgap Domains",
        description="Provides the ability to update stopgap domains records within context.",
        resource_types=[
            ResourceTypeEnum.system_stopgap_domain,
        ],
    )
    """Provides the ability to update stopgap domains records within context."""

    system_stopgap_domains_delete: Permission = Permission(
        uri="system:stopgap_domains:delete",
        title="Delete Stopgap Domains",
        description="Provides the ability to delete stopgap domain records within context.",
        resource_types=[
            ResourceTypeEnum.system_stopgap_domain,
        ],
    )
    """Provides the ability to delete stopgap domains records within context."""

    system_timezones: Permission = Permission(
        uri="system:timezones",
        title="All Timezones Permissions",
        description="Includes all timezones-related permissions.",
        resource_types=[
            ResourceTypeEnum.system_timezone,
        ],
    )
    """Includes all timezones-related permissions."""

    system_timezones_read: Permission = Permission(
        uri="system:timezones:read",
        title="Read Timezones",
        description="Provides the ability to read timezone records within context.",
        resource_types=[
            ResourceTypeEnum.system_timezone,
        ],
    )
    """Provides the ability to read timezone records within context."""

    system_timezones_create: Permission = Permission(
        uri="system:timezones:create",
        title="Create Timezones",
        description="Provides the ability to create timezone records within context.",
        resource_types=[
            ResourceTypeEnum.system_timezone,
        ],
    )
    """Provides the ability to create timezone records within context."""

    system_timezones_update: Permission = Permission(
        uri="system:timezones:update",
        title="Update Timezones",
        description="Provides the ability to update timezone records within context.",
        resource_types=[
            ResourceTypeEnum.system_timezone,
        ],
    )
    """Provides the ability to update timezone records within context."""

    system_timezones_delete: Permission = Permission(
        uri="system:timezones:delete",
        title="Delete Timezones",
        description="Provides the ability to delete timezone records within context.",
        resource_types=[
            ResourceTypeEnum.system_timezone,
        ],
    )
    """Provides the ability to delete timezone records within context."""

    tenants: Permission = Permission(
        uri="tenants:tenant",
        title="All Tenants Permissions",
        description="Includes all tenants-related permissions.",
        resource_types=[
            ResourceTypeEnum.tenants_tenant,
        ],
    )
    """Includes all tenants-related permissions."""

    tenants_read: Permission = Permission(
        uri="tenants:tenant:read",
        title="Read Tenants",
        description="Provides the ability to read tenant records within context.",
        resource_types=[
            ResourceTypeEnum.tenants_tenant,
        ],
    )
    """Provides the ability to read tenant records within context."""

    tenants_create: Permission = Permission(
        uri="tenants:tenant:create",
        title="Create Tenants",
        description="Provides the ability to create tenant records within context.",
        resource_types=[
            ResourceTypeEnum.tenants_tenant,
        ],
    )
    """Provides the ability to create tenant records within context."""

    tenants_update: Permission = Permission(
        uri="tenants:tenant:update",
        title="Update Tenants",
        description="Provides the ability to update tenant records within context.",
        resource_types=[
            ResourceTypeEnum.tenants_tenant,
        ],
    )
    """Provides the ability to update tenant records within context."""

    tenants_delete: Permission = Permission(
        uri="tenants:tenant:delete",
        title="Delete Tenants",
        description="Provides the ability to delete tenant records within context.",
        resource_types=[
            ResourceTypeEnum.tenants_tenant,
        ],
    )
    """Provides the ability to delete tenant records within context."""

    servers: Permission = Permission(
        uri="servers:server",
        title="All Servers Permissions",
        description="Includes all servers-related permissions.",
        resource_types=[
            ResourceTypeEnum.servers_server,
        ],
    )
    """Includes all servers-related permissions."""

    servers_read: Permission = Permission(
        uri="servers:server:read",
        title="Read Servers",
        description="Provides the ability to read server records within context.",
        resource_types=[
            ResourceTypeEnum.servers_server,
        ],
    )
    """Provides the ability to read server records within context."""

    servers_create: Permission = Permission(
        uri="servers:server:create",
        title="Create Servers",
        description="Provides the ability to create server records within context.",
        resource_types=[
            ResourceTypeEnum.servers_server,
        ],
    )
    """Provides the ability to create server records within context."""

    servers_update: Permission = Permission(
        uri="servers:server:update",
        title="Update Servers",
        description="Provides the ability to update server records within context.",
        resource_types=[
            ResourceTypeEnum.servers_server,
        ],
    )
    """Provides the ability to update server records within context."""

    servers_delete: Permission = Permission(
        uri="servers:server:delete",
        title="Delete Servers",
        description="Provides the ability to delete server records within context.",
        resource_types=[
            ResourceTypeEnum.servers_server,
        ],
    )
    """Provides the ability to delete server records within context."""

    servers_auto_primary: Permission = Permission(
        uri="servers:auto_primary",
        title="All Server Auto-Primaries Permissions",
        description="Includes all server auto-primary-related permissions.",
        resource_types=[
            ResourceTypeEnum.servers_auto_primary,
        ],
    )
    """Includes all server auto-primary-related permissions."""

    servers_auto_primary_read: Permission = Permission(
        uri="servers:auto_primary:read",
        title="Read Server Auto-Primaries",
        description="Provides the ability to read server records within context.",
        resource_types=[
            ResourceTypeEnum.servers_auto_primary,
        ],
    )
    """Provides the ability to read server records within context."""

    servers_auto_primary_create: Permission = Permission(
        uri="servers:auto_primary:create",
        title="Create Server Auto-Primaries",
        description="Provides the ability to create server records within context.",
        resource_types=[
            ResourceTypeEnum.servers_auto_primary,
        ],
    )
    """Provides the ability to create server records within context."""

    servers_auto_primary_update: Permission = Permission(
        uri="servers:auto_primary:update",
        title="Update Server Auto-Primaries",
        description="Provides the ability to update server records within context.",
        resource_types=[
            ResourceTypeEnum.servers_auto_primary,
        ],
    )
    """Provides the ability to update server records within context."""

    servers_auto_primary_delete: Permission = Permission(
        uri="servers:auto_primary:delete",
        title="Delete Server Auto-Primaries",
        description="Provides the ability to delete server records within context.",
        resource_types=[
            ResourceTypeEnum.servers_auto_primary,
        ],
    )
    """Provides the ability to delete server records within context."""

    keys_crypto_keys: Permission = Permission(
        uri="keys:crypto_key",
        title="All Crypto Keys Permissions",
        description="Includes all crypto keys-related permissions.",
        resource_types=[
            ResourceTypeEnum.keys_crypto_key,
        ],
    )
    """Includes all crypto keys-related permissions."""

    keys_crypto_keys_read: Permission = Permission(
        uri="keys:crypto_key:read",
        title="Read Crypto Keys",
        description="Provides the ability to read crypto key records within context.",
        resource_types=[
            ResourceTypeEnum.keys_crypto_key,
        ],
    )
    """Provides the ability to read crypto key records within context."""

    keys_crypto_keys_create: Permission = Permission(
        uri="keys:crypto_key:create",
        title="Create Crypto Keys",
        description="Provides the ability to create crypto key records within context.",
        resource_types=[
            ResourceTypeEnum.keys_crypto_key,
        ],
    )
    """Provides the ability to create crypto key records within context."""

    keys_crypto_keys_update: Permission = Permission(
        uri="keys:crypto_key:update",
        title="Update Crypto Keys",
        description="Provides the ability to update crypto key records within context.",
        resource_types=[
            ResourceTypeEnum.keys_crypto_key,
        ],
    )
    """Provides the ability to update crypto key records within context."""

    keys_crypto_keys_delete: Permission = Permission(
        uri="keys:crypto_key:delete",
        title="Delete Crypto Keys",
        description="Provides the ability to delete crypto key records within context.",
        resource_types=[
            ResourceTypeEnum.keys_crypto_key,
        ],
    )
    """Provides the ability to delete crypto key records within context."""

    keys_tsig_keys: Permission = Permission(
        uri="keys:tsig_key",
        title="All TSIG Keys Permissions",
        description="Includes all TSIG keys-related permissions.",
        resource_types=[
            ResourceTypeEnum.keys_tsig_key,
        ],
    )
    """Includes all TSIG keys-related permissions."""

    keys_tsig_keys_read: Permission = Permission(
        uri="keys:tsig_key:read",
        title="Read TSIG Keys",
        description="Provides the ability to read TSIG key records within context.",
        resource_types=[
            ResourceTypeEnum.keys_tsig_key,
        ],
    )
    """Provides the ability to read TSIG key records within context."""

    keys_tsig_keys_create: Permission = Permission(
        uri="keys:tsig_key:create",
        title="Create TSIG Keys",
        description="Provides the ability to create TSIG key records within context.",
        resource_types=[
            ResourceTypeEnum.keys_tsig_key,
        ],
    )
    """Provides the ability to create TSIG key records within context."""

    keys_tsig_keys_update: Permission = Permission(
        uri="keys:tsig_key:update",
        title="Update TSIG Keys",
        description="Provides the ability to update TSIG key records within context.",
        resource_types=[
            ResourceTypeEnum.keys_tsig_key,
        ],
    )
    """Provides the ability to update TSIG key records within context."""

    keys_tsig_keys_delete: Permission = Permission(
        uri="keys:tsig_key:delete",
        title="Delete TSIG Keys",
        description="Provides the ability to delete TSIG key records within context.",
        resource_types=[
            ResourceTypeEnum.keys_tsig_key,
        ],
    )
    """Provides the ability to delete TSIG key records within context."""

    zones_azone: Permission = Permission(
        uri="zones:azone",
        title="All Authoritative Zones Permissions",
        description="Includes all authoritative zones-related permissions.",
        resource_types=[
            ResourceTypeEnum.zones_azone,
        ],
    )
    """Includes all authoritative zones-related permissions."""

    zones_azone_read: Permission = Permission(
        uri="zones:azone:read",
        title="Read Authoritative Zones",
        description="Provides the ability to read authoritative zone records within context.",
        resource_types=[
            ResourceTypeEnum.zones_azone,
        ],
    )
    """Provides the ability to read authoritative zone records within context."""

    zones_azone_create: Permission = Permission(
        uri="zones:azone:create",
        title="Create Authoritative Zones",
        description="Provides the ability to create authoritative zone records within context.",
        resource_types=[
            ResourceTypeEnum.zones_azone,
        ],
    )
    """Provides the ability to create authoritative zone records within context."""

    zones_azone_update: Permission = Permission(
        uri="zones:azone:update",
        title="Update Authoritative Zones",
        description="Provides the ability to update authoritative zone records within context.",
        resource_types=[
            ResourceTypeEnum.zones_azone,
        ],
    )
    """Provides the ability to update authoritative zone records within context."""

    zones_azone_delete: Permission = Permission(
        uri="zones:azone:delete",
        title="Delete Authoritative Zones",
        description="Provides the ability to delete authoritative zone records within context.",
        resource_types=[
            ResourceTypeEnum.zones_azone,
        ],
    )
    """Provides the ability to delete authoritative zone records within context."""

    # TODO: Authoritative Zone Records, Metadata

    zones_rzone: Permission = Permission(
        uri="zones:rzone",
        title="All Recursive Zones Permissions",
        description="Includes all recursive zones-related permissions.",
        resource_types=[
            ResourceTypeEnum.zones_rzone,
        ],
    )
    """Includes all recursive zones-related permissions."""

    zones_rzone_read: Permission = Permission(
        uri="zones:rzone:read",
        title="Read Recursive Zones",
        description="Provides the ability to read recursive zone records within context.",
        resource_types=[
            ResourceTypeEnum.zones_rzone,
        ],
    )
    """Provides the ability to read recursive zone records within context."""

    zones_rzone_create: Permission = Permission(
        uri="zones:rzone:create",
        title="Create Recursive Zones",
        description="Provides the ability to create recursive zone records within context.",
        resource_types=[
            ResourceTypeEnum.zones_rzone,
        ],
    )
    """Provides the ability to create recursive zone records within context."""

    zones_rzone_update: Permission = Permission(
        uri="zones:rzone:update",
        title="Update Recursive Zones",
        description="Provides the ability to update recursive zone records within context.",
        resource_types=[
            ResourceTypeEnum.zones_rzone,
        ],
    )
    """Provides the ability to update recursive zone records within context."""

    zones_rzone_delete: Permission = Permission(
        uri="zones:rzone:delete",
        title="Delete Recursive Zones",
        description="Provides the ability to delete recursive zone records within context.",
        resource_types=[
            ResourceTypeEnum.zones_rzone,
        ],
    )
    """Provides the ability to delete recursive zone records within context."""

    # TODO: Recursive Zone Records

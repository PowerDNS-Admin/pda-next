"""
PDA ACL Database Models

This file defines the database models associated with ACL functionality.
"""
import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import DateTime, String, TEXT, Uuid, text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import BaseSqlModel


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


class Role(BaseSqlModel):
    """Represents an ACL role."""

    __tablename__ = 'pda_acl_roles'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    slug: Mapped[str] = mapped_column(String(50), nullable=False)
    """The role slug."""

    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    """The description of the role."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    permissions = relationship('RolePermission', back_populates='role')
    """A list of permissions associated with the role."""


class RolePermission(BaseSqlModel):
    """Represents an ACL role permission."""

    __tablename__ = 'pda_acl_role_permissions'
    """Defines the database table name."""

    role_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_acl_roles.id'), nullable=False)
    """The unique identifier of the associated role."""

    permission: Mapped[PermissionEnum] = mapped_column(TEXT, nullable=False)
    """The permission associated with the role."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    role = relationship('Role', back_populates='permissions')
    """The role associated with the permission."""

    __mapper_args__ = {
        'primary_key': [role_id, permission],
    }


class Acl(BaseSqlModel):
    """Represents an ACL."""

    __tablename__ = 'pda_acls'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    resource_type: Mapped[ResourceTypeEnum] = mapped_column(String(20), nullable=False)
    """The resource type associated with the ACL."""

    resource_id: Mapped[str] = mapped_column(Uuid, nullable=False)
    """The unique identifier of the associated resource."""

    principal_type: Mapped[PrincipalTypeEnum] = mapped_column(String(20), nullable=False)
    """The principal type associated with the ACL."""

    principal_id: Mapped[str] = mapped_column(Uuid, nullable=False)
    """The unique identifier of the associated principal."""

    permission: Mapped[PermissionEnum] = mapped_column(String(255), nullable=False)
    """The permission associated with the ACL."""

    created_by: Mapped[str] = mapped_column(
        Uuid, ForeignKey('pda_auth_users.id'), nullable=False,
    )
    """The unique identifier of the user that created the ACL."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    __table_args__ = (
        UniqueConstraint(
            'resource_type', 'resource_id', 'principal_type', 'principal_id', 'permission', name='uix_acl'
        ),
    )

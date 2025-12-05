"""
PDA ACL Database Models

This file defines the database models associated with ACL functionality.
"""
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import DateTime, String, TEXT, Uuid, text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.db import BaseSqlModel
from models.enums import ResourceTypeEnum, PrincipalTypeEnum


class Role(BaseSqlModel):
    """Represents an ACL role."""

    __tablename__ = 'pda_acl_roles'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the role."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey(
        'pda_tenants.id', onupdate='CASCADE', ondelete='CASCADE'
    ), nullable=True)
    """The unique identifier of the associated tenant if any."""

    slug: Mapped[str] = mapped_column(String(50), nullable=False)
    """The role slug."""

    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    """The description of the role."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the role was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the role was last updated."""

    tenant = relationship('Tenant', back_populates='acl_roles', cascade='expunge, delete')
    """The tenant associated with the role."""

    permissions = relationship('RolePermission', back_populates='role', cascade='all, delete, delete-orphan')
    """A list of permissions associated with the role."""

    principals = relationship('RolePrincipal', back_populates='role', cascade='all, delete, delete-orphan')
    """A list of principals associated with the role."""


class RolePermission(BaseSqlModel):
    """Represents an ACL role permission relationship."""

    __tablename__ = 'pda_acl_role_permissions'
    """Defines the database table name."""

    role_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey(
        'pda_acl_roles.id', onupdate='CASCADE', ondelete='CASCADE'
    ), nullable=False)
    """The unique identifier of the associated role."""

    permission: Mapped[str] = mapped_column(TEXT, nullable=False)
    """The permission associated with the role."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the role permission was created."""

    role = relationship('Role', back_populates='permissions', cascade='expunge, delete')
    """The role associated with the permission."""

    __mapper_args__ = {
        'primary_key': [role_id, permission],
    }


class RolePrincipal(BaseSqlModel):
    """Represents an ACL role principal relationship."""

    __tablename__ = 'pda_acl_role_principals'
    """Defines the database table name."""

    role_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey(
        'pda_acl_roles.id', onupdate='CASCADE', ondelete='CASCADE'
    ), nullable=False)
    """The unique identifier of the associated role."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey(
        'pda_tenants.id', onupdate='CASCADE', ondelete='CASCADE'
    ), nullable=True)
    """The unique identifier of the associated tenant if any."""

    principal_type: Mapped[PrincipalTypeEnum] = mapped_column(String(20), nullable=False)
    """The principal type associated with the principal relationship."""

    principal_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    """The unique identifier of the associated principal."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the principal relationship was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the principal relationship was last updated."""

    role = relationship('Role', back_populates='principals', cascade='expunge, delete')
    """The role associated with the principal relationship."""

    tenant = relationship('Tenant', back_populates='acl_role_principals', cascade='expunge, delete')
    """The tenant associated with the principal relationship."""

    __mapper_args__ = {
        'primary_key': [role_id, principal_id],
    }


class Policy(BaseSqlModel):
    """Represents an ACL policy."""

    __tablename__ = 'pda_acl_policies'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the policy."""

    resource_type: Mapped[ResourceTypeEnum] = mapped_column(String(20), nullable=False)
    """The resource type associated with the policy."""

    resource_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    """The unique identifier of the associated resource."""

    principal_type: Mapped[PrincipalTypeEnum] = mapped_column(String(20), nullable=False)
    """The principal type associated with the policy."""

    principal_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    """The unique identifier of the associated principal."""

    permission: Mapped[str] = mapped_column(String(255), nullable=False)
    """The permission associated with the policy."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the policy was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the policy was last updated."""

    __table_args__ = (
        UniqueConstraint(
            'resource_type', 'resource_id', 'principal_type', 'principal_id', 'permission', name='uix_acl'
        ),
    )

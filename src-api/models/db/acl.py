"""
PDA ACL Database Models

This file defines the database models associated with ACL functionality.
"""
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import DateTime, String, Boolean, Enum, TEXT, Uuid, text, ForeignKey, UniqueConstraint
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

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    """The role name."""

    description: Mapped[str] = mapped_column(TEXT, nullable=True)
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

    parents: Mapped[list['RoleInheritance']] = relationship(
        'RoleInheritance',
        foreign_keys='[RoleInheritance.child_role_id]',
        back_populates='child',
        cascade='all, delete-orphan',
    )
    """The parent roles associated with the role."""

    principals = relationship('RolePrincipal', back_populates='role', cascade='all, delete, delete-orphan')
    """A list of principals associated with the role."""


class RoleInheritance(BaseSqlModel):
    """Represents an ACL role hierarchy connection."""

    __tablename__ = 'pda_acl_role_inheritance'
    """Defines the database table name."""

    child_role_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_acl_roles.id'), primary_key=True)
    """The unique identifier of the child role."""

    parent_role_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_acl_roles.id'), primary_key=True)
    """The unique identifier of the parent role."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the connection was created."""

    child: Mapped[Role] = relationship(
        'Role', foreign_keys=[child_role_id], back_populates='parents', cascade='expunge, delete'
    )
    """The child role of the connection."""

    parent: Mapped[Role] = relationship(
        'Role', foreign_keys=[parent_role_id], cascade='expunge, delete'
    )
    """The child role of the connection."""


class Principal(BaseSqlModel):
    """Represents an ACL Principal."""

    __tablename__ = 'pda_acl_principals'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the principal."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey(
        'pda_tenants.id', onupdate='CASCADE', ondelete='CASCADE'
    ), nullable=True)
    """The unique identifier of the associated tenant if any."""

    type: Mapped[PrincipalTypeEnum] = mapped_column(Enum(PrincipalTypeEnum, native_enum=False), nullable=False)
    """The principal type associated with the principal."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the role was created."""

    roles: Mapped[list['PrincipalRoleAssoc']] = relationship(
        'PrincipalRoleAssoc',
        back_populates='principal',
        cascade='all, delete-orphan',
    )
    """The parent roles associated with the role."""


class PrincipalRoleAssoc(BaseSqlModel):
    """Represents an ACL principal role association."""

    __tablename__ = 'pda_acl_principal_role_assoc'
    """Defines the database table name."""

    principal_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_acl_principals.id'), primary_key=True)
    """The unique identifier of the associated principal role."""

    role_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('pda_acl_roles.id'), primary_key=True)
    """The unique identifier of the associated role."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the association was created."""

    principal: Mapped[Principal] = relationship('Principal', back_populates='roles')
    """The principal of the association."""

    role: Mapped[Role] = relationship('Role')
    """The role of the association."""


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

    role = relationship('Role', back_populates='principals', cascade='expunge, delete')
    """The role associated with the principal relationship."""

    __mapper_args__ = {
        'primary_key': [role_id, principal_id],
    }


class Policy(BaseSqlModel):
    """Represents an ACL policy."""

    __tablename__ = 'pda_acl_policies'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the policy."""

    tenant_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey(
        'pda_tenants.id', onupdate='CASCADE', ondelete='CASCADE'
    ), nullable=True)
    """The unique identifier of the associated tenant if any."""

    resource_type: Mapped[ResourceTypeEnum] = mapped_column(Enum(ResourceTypeEnum, native_enum=False), nullable=False)
    """The resource type associated with the policy."""

    resource_id: Mapped[UUID] = mapped_column(Uuid, nullable=True)
    """The unique identifier of the associated resource if any."""

    principal_type: Mapped[PrincipalTypeEnum] = mapped_column(String(20), nullable=False)
    """The principal type associated with the policy."""

    principal_id: Mapped[UUID] = mapped_column(Uuid, nullable=True)
    """The unique identifier of the associated principal if any."""

    permission: Mapped[str] = mapped_column(String(255), nullable=False)
    """The permission associated with the policy."""

    deny: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Determines if the policy is an allow or deny policy."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the policy was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the policy was last updated."""

    tenant = relationship('Tenant', back_populates='acl_policies', cascade='expunge, delete')
    """The tenant associated with the policy."""

    __table_args__ = (
        UniqueConstraint(
            'tenant_id', 'resource_type', 'resource_id', 'principal_type', 'principal_id', 'permission',
            name='uix_acl',
        ),
    )

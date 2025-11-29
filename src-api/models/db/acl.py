"""
PDA ACL Database Models

This file defines the database models associated with ACL functionality.
"""
import uuid
from datetime import datetime
from sqlalchemy import DateTime, String, TEXT, Uuid, text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.db import BaseSqlModel
from models.enums import ResourceTypeEnum, PrincipalTypeEnum, PermissionEnum


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

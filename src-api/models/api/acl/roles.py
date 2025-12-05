from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field, field_validator

from lib.permissions.definitions import Permissions
from models.api import BaseApiModel



class RoleInSchema(BaseApiModel):
    """Provides an API input model for creating and updating ACL roles."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the role if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the role if any."""

    slug: str = Field(
        title='Role Slug',
        description='The slug of the role.',
        examples=['system_admin', 'tenant_admin', 'tenant_owner', 'zone_admin'],
    )
    """The slug of the role."""

    description: str = Field(
        title='Role Description',
        description='The description of the role.',
        examples=[
            'Provides permissions for system administrators.',
            'Provides permissions for tenant administrators.',
            'Provides permissions for tenant owners.',
            'Provides permissions for zone managers.',
        ],
    )
    """The description of the role."""

    permissions: set[str] = Field(
        title='Role Permissions',
        description='The permissions associated with the role.',
        default_factory=set[str],
        examples=[[
            Permissions.auth_users.uri,
            Permissions.auth_clients_read.uri,
            Permissions.zones_azone_update.uri,
        ]],
    )
    """The permissions associated with the role."""

    @field_validator('permissions')
    @classmethod
    def permissions_validator(cls, v: list[str]) -> list[str]:
        """Validates that the given permissions exist."""
        if not v:
            raise ValueError('At least one permission is required for a role')

        permissions = Permissions.scopes

        for permission in v:
            if permission not in permissions:
                raise ValueError(f'Invalid permission "{permission}"')

        return v


class RolePermissionOutSchema(BaseApiModel):
    """Provides an API response model for representing ACL role permissions."""

    permission: str = Field(
        title='Permission URI',
        description='The URI of the associated permission.',
        examples=[
            Permissions.auth_users.uri,
            Permissions.auth_clients_read.uri,
            Permissions.zones_azone_update.uri,
        ],
    )
    """The URI of the associated permission."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the association was created.',
        default_factory=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the association was created."""


class RoleOutSchema(BaseApiModel):
    """Provides an API response model for representing ACL roles."""

    id: UUID = Field(
        title='Role ID',
        description='The unique identifier of the role.',
        default_factory=uuid4,
        examples=[uuid4()],
    )
    """The unique identifier of the role."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the role if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the role if any."""

    slug: str = Field(
        title='Role Slug',
        description='The slug of the role.',
        examples=['system_admin', 'tenant_admin', 'tenant_owner', 'zone_admin'],
    )
    """The slug of the role."""

    description: str = Field(
        title='Role Description',
        description='The description of the role.',
        examples=[
            'Provides permissions for system administrators.',
            'Provides permissions for tenant administrators.',
            'Provides permissions for tenant owners.',
            'Provides permissions for zone managers.',
        ],
    )
    """The description of the role."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the role was created.',
        default_factory=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the role was created."""

    updated_at: datetime = Field(
        title='Updated At',
        description='The timestamp representing when the role was last updated.',
        default_factory=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the role was last updated."""

    permissions: Optional[list[RolePermissionOutSchema]] = Field(
        title='Role Permissions',
        description='The permissions associated with the role.',
        default_factory=list[RolePermissionOutSchema],
        examples=[
            RolePermissionOutSchema(permission=Permissions.auth_users.uri),
            RolePermissionOutSchema(permission=Permissions.auth_clients_read.uri),
            RolePermissionOutSchema(permission=Permissions.zones_azone_update.uri),
        ],
    )
    """The permissions associated with the role."""


class RolesSchema(BaseApiModel):
    """Provides an API response model for retrieving ACL roles."""

    records: list[RoleOutSchema] = Field(
        title='Roles',
        description='A list of roles found based on the current request criteria.',
        default_factory=list[RoleOutSchema],
        examples=[[
            RoleOutSchema(slug='system_admin', description='A role for system administrators.'),
            RoleOutSchema(slug='tenant_admin', description='A role for tenant administrators.'),
            RoleOutSchema(slug='tenant_owner', description='A role for tenant owners.'),
            RoleOutSchema(slug='zone_admin', description='A role for zone administrators.'),
        ]],
    )
    """A list of roles found based on the current request criteria."""

    total: int = Field(
        title='Total Roles Found',
        description='The total number of roles found based on the current request criteria.',
        default=0,
        examples=[4],
    )
    """The total number of roles found based on the current request criteria."""

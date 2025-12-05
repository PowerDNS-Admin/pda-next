from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field, field_validator

from lib.permissions.definitions import Permissions
from models.api import BaseApiModel
from models.enums import ResourceTypeEnum, PrincipalTypeEnum


class PolicyInSchema(BaseApiModel):
    """Provides an API input model for creating and updating ACL policies."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the policy if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the policy if any."""

    resource_type: ResourceTypeEnum = Field(
        title='Resource Type',
        description='The resource type associated with the policy.',
        examples=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_client,
            ResourceTypeEnum.auth_session,
            ResourceTypeEnum.zones_azone,
            ResourceTypeEnum.zones_rzone,
        ],
    )
    """The resource type associated with the policy."""

    resource_id: Optional[UUID] = Field(
        title='Resource ID',
        description='The unique identifier of the resource associated with the policy if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the resource associated with the policy if any."""

    principal_type: PrincipalTypeEnum = Field(
        title='Principal Type',
        description='The principal type associated with the policy.',
        examples=[
            PrincipalTypeEnum.role,
            PrincipalTypeEnum.tenant,
            PrincipalTypeEnum.client,
            PrincipalTypeEnum.user,
        ],
    )
    """The principal type associated with the policy."""

    principal_id: Optional[UUID] = Field(
        title='Principal ID',
        description='The unique identifier of the principal associated with the policy if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the principal associated with the policy if any."""

    permission: str = Field(
        title='Permission',
        description='The permission associated with the policy.',
        examples=[
            Permissions.auth_users.uri,
            Permissions.auth_clients_read.uri,
            Permissions.zones_azone_record_update.uri,
        ],
    )
    """The permission associated with the policy."""

    @field_validator('permission')
    @classmethod
    def permission_validator(cls, v: str) -> str:
        """Validates that the given permission exists."""
        permissions = Permissions.scopes

        if v not in permissions:
            raise ValueError(f'Invalid permission "{v}"')

        return v


class PolicyOutSchema(BaseApiModel):
    """Provides an API response model for representing ACL policies."""

    id: UUID = Field(
        title='Policy ID',
        description='The unique identifier of the policy.',
        default_factory=uuid4,
        examples=[uuid4()],
    )
    """The unique identifier of the policy."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the policy if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the policy if any."""

    resource_type: ResourceTypeEnum = Field(
        title='Resource Type',
        description='The resource type associated with the policy.',
        examples=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_client,
            ResourceTypeEnum.auth_session,
            ResourceTypeEnum.zones_azone,
            ResourceTypeEnum.zones_rzone,
        ],
    )
    """The resource type associated with the policy."""

    resource_id: Optional[UUID] = Field(
        title='Resource ID',
        description='The unique identifier of the resource associated with the policy if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the resource associated with the policy if any."""

    principal_type: PrincipalTypeEnum = Field(
        title='Principal Type',
        description='The principal type associated with the policy.',
        examples=[
            PrincipalTypeEnum.role,
            PrincipalTypeEnum.tenant,
            PrincipalTypeEnum.client,
            PrincipalTypeEnum.user,
        ],
    )
    """The principal type associated with the policy."""

    principal_id: Optional[UUID] = Field(
        title='Principal ID',
        description='The unique identifier of the principal associated with the policy if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the principal associated with the policy if any."""

    permission: str = Field(
        title='Permission',
        description='The permission associated with the policy.',
        examples=[
            Permissions.auth_users.uri,
            Permissions.auth_clients_read.uri,
            Permissions.zones_azone_record_update.uri,
        ],
    )
    """The permission associated with the policy."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the policy was created.',
        default_factory=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the policy was created."""

    updated_at: datetime = Field(
        title='Updated At',
        description='The timestamp representing when the policy was last updated.',
        default_factory=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the policy was last updated."""


class PoliciesSchema(BaseApiModel):
    """Provides an API response model for retrieving ACL policies."""

    records: list[PolicyOutSchema] = Field(
        title='Policies',
        description='A list of policies found based on the current request criteria.',
        default_factory=list[PolicyOutSchema],
        examples=[[
            PolicyOutSchema(
                resource_type=ResourceTypeEnum.auth_user,
                resource_id=uuid4(),
                principal_type=PrincipalTypeEnum.client,
                principal_id=uuid4(),
                permission=Permissions.auth_users.uri,
            ),
            PolicyOutSchema(
                resource_type=ResourceTypeEnum.auth_user,
                resource_id=uuid4(),
                principal_type=PrincipalTypeEnum.user,
                principal_id=uuid4(),
                permission=Permissions.auth_users_read.uri,
            ),
            PolicyOutSchema(
                resource_type=ResourceTypeEnum.zones_azone,
                resource_id=uuid4(),
                principal_type=PrincipalTypeEnum.role,
                principal_id=uuid4(),
                permission=Permissions.zones_azone_read.uri,
            ),
            PolicyOutSchema(
                resource_type=ResourceTypeEnum.zones_azone,
                resource_id=uuid4(),
                principal_type=PrincipalTypeEnum.tenant,
                principal_id=uuid4(),
                permission=Permissions.zones_azone.uri,
            ),
        ]],
    )
    """A list of policies found based on the current request criteria."""

    total: int = Field(
        title='Total Policies Found',
        description='The total number of policies found based on the current request criteria.',
        default=0,
        examples=[4],
    )
    """The total number of policies found based on the current request criteria."""

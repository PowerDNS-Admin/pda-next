from typing import Optional

from pydantic import Field

from models.api import BaseApiModel
from models.enums import PrincipalTypeEnum, ResourceTypeEnum


class Permission(BaseApiModel):
    """Provides an interface for defining a system permission and applying it accordingly."""

    uri: str = Field(
        title='Permission URI',
        description='The uniform resource identifier (URI) used in policy definition and assignment storage to represent the permission.',
        pattern=r'^[a-z]+(?:[:][a-z0-9_]+)?$',
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

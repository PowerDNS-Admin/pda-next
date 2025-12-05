from pydantic import Field, computed_field

from lib.permissions.definitions import Permission, Permissions
from models.api import BaseApiModel


class PermissionsMetadataSchema(BaseApiModel):
    """Provides an API response model for retrieving ACL permissions metadata."""

    permissions: list[Permission] = Field(
        title='Permissions',
        description='A list of permission definitions.',
        default=Permissions.all,
        examples=[[
            Permissions.auth_users,
            Permissions.auth_clients,
            Permissions.zones_azone_read,
            Permissions.zones_rzone_update,
        ]],
    )
    """A list of permission definitions."""

    @computed_field(
        title='Total Permissions',
        description='The total number of permissions.',
        examples=[4],
    )
    @property
    def total(self) -> int:
        """Returns the total number of permissions."""
        return len(self.permissions)

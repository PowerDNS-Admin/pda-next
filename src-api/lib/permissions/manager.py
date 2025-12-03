from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from lib.permissions.definitions import Permission
from models.api.auth import Principal
from models.enums import ResourceTypeEnum


class PermissionsManager:
    """Provides an interface for managing and validating permissions."""

    @staticmethod
    async def has_permission(
            db: AsyncSession,
            principal: Principal,
            resource_type: ResourceTypeEnum,
            resource_id: str | UUID,
            permissions: Permission | list[Permission],
    ) -> bool:
        """Verifies if the given principal has the given permission for the given resource."""
        from loguru import logger

        if isinstance(resource_id, str):
            resource_id = UUID(resource_id)

        if isinstance(permissions, Permission):
            permissions = [permissions]

        permission_strings = set(p.uri for p in permissions)

        logger.warning(f'Validating permissions: principal: {principal.type.value}({principal.id}), '
                       + f'resource: {resource_type.value}({resource_id}), permissions: {permission_strings}')

        # TODO

        return False

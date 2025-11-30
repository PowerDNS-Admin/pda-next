from models.api.acl import Permission
from models.enums import ResourceTypeEnum


class classproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, owner):
        # Call the decorated function with the class object (owner)
        return self.func(owner)


class Permissions:
    """Defines the available permissions of the system."""

    @classproperty
    def scopes(cls) -> dict[str, str]:
        """Provides a dictionary of available permissions in the form of OAuth API scopes."""
        return {p.uri: p.title for k, p in cls.__dict__.items() if not k.startswith('__') and k != 'scopes'}

    users: Permission = Permission(
        uri="users",
        title="All Users Permissions",
        description="Includes all users-related permissions.",
        resource_types=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_user_authenticator,
        ],
    )
    """Includes all users-related permissions."""

    users_read: Permission = Permission(
        uri="users:read",
        title="Read Users",
        description="Provides the ability to read user records within context.",
        resource_types=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_user_authenticator,
        ],
    )
    """Provides the ability to read user records within context."""

    users_create: Permission = Permission(
        uri="users:create",
        title="Create Users",
        description="Provides the ability to create user records within context.",
        resource_types=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_user_authenticator,
        ],
    )
    """Provides the ability to create user records within context."""

    users_update: Permission = Permission(
        uri="users:update",
        title="Update Users",
        description="Provides the ability to update user records within context.",
        resource_types=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_user_authenticator,
        ],
    )
    """Provides the ability to update user records within context."""

    users_delete: Permission = Permission(
        uri="users:delete",
        title="Delete Users",
        description="Provides the ability to delete user records within context.",
        resource_types=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_user_authenticator,
        ],
    )
    """Provides the ability to delete user records within context."""

    users_reset_password: Permission = Permission(
        uri="users:reset_password",
        title="Reset User Passwords",
        description="Provides the ability to reset user passwords within context.",
        resource_types=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_user_authenticator,
        ],
    )
    """Provides the ability to reset user passwords within context."""

    users_change_status: Permission = Permission(
        uri="users:change_status",
        title="Change User Statuses",
        description="Provides the ability to change a user's status within context.",
        resource_types=[
            ResourceTypeEnum.auth_user,
            ResourceTypeEnum.auth_user_authenticator,
        ],
    )
    """Provides the ability to change a user's status within context."""

    roles: Permission = Permission(
        uri="roles",
        title="All Roles Permissions",
        description="Includes all roles-related permissions.",
        resource_types=[
            ResourceTypeEnum.acl_role,
            ResourceTypeEnum.acl_acl,
        ],
    )
    """Includes all roles-related permissions."""

    roles_read: Permission = Permission(
        uri="roles:read",
        title="Read Roles",
        description="Provides the ability to read role records within context.",
        resource_types=[
            ResourceTypeEnum.acl_role,
            ResourceTypeEnum.acl_acl,
        ],
    )
    """Provides the ability to read role records within context."""

    roles_create: Permission = Permission(
        uri="roles:create",
        title="Create Roles",
        description="Provides the ability to create role records within context.",
        resource_types=[
            ResourceTypeEnum.acl_role,
            ResourceTypeEnum.acl_acl,
        ],
    )
    """Provides the ability to create role records within context."""

    roles_update: Permission = Permission(
        uri="roles:update",
        title="Update Roles",
        description="Provides the ability to update role records within context.",
        resource_types=[
            ResourceTypeEnum.acl_role,
            ResourceTypeEnum.acl_acl,
        ],
    )
    """Provides the ability to update role records within context."""

    roles_delete: Permission = Permission(
        uri="roles:delete",
        title="Delete Roles",
        description="Provides the ability to delete role records within context.",
        resource_types=[
            ResourceTypeEnum.acl_role,
            ResourceTypeEnum.acl_acl,
        ],
    )
    """Provides the ability to delete role records within context."""

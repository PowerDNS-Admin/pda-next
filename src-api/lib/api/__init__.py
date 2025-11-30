from models.enums import PermissionEnum

API_SCOPES = {
    PermissionEnum.auth_all.value: 'Full access to authentication features.',
    PermissionEnum.auth_user_all.value: 'Full access to user administration.',
    PermissionEnum.auth_user_list.value: 'Ability to list users.',
    PermissionEnum.auth_user_create.value: 'Ability to create users.',
    PermissionEnum.auth_user_read.value: 'Ability to read users.',
    PermissionEnum.auth_user_update.value: 'Ability to update users.',
    PermissionEnum.auth_user_delete.value: 'Ability to delete users.',
}

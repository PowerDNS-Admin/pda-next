
export interface UserInfo {
    id: string;
    tenantId?: string | null;
    displayName?: string | null;
    username: string | null;
    email?: string | null;
    phoneNumber?: string | null;
    photoURL?: string | null;
    status: string | null;
    createdAt?: string;
    updatedAt?: string;
    authenticatedAt?: string;
}

export interface User extends UserInfo {
    readonly tenantId?: string | null;
    password?: string | null;
}

export type IUser = User;

import {IUser} from '@app/types/user';

type AuthCallback = (user: IUser | null) => void;

class AuthService {
    private currentUser: IUser | null = null;
    private subscribers: Set<AuthCallback> = new Set();

    // Similar to Firebase onAuthStateChanged
    onAuthStateChanged(callback: AuthCallback): () => void {
        this.subscribers.add(callback);

        // Immediately call with current state (Firebase does this)
        callback(this.currentUser);

        // Unsubscribe function
        return () => {
            this.subscribers.delete(callback);
        };
    }

    private emit(user: IUser | null) {
        this.currentUser = user;
        for (const cb of this.subscribers) cb(user);
    }

    async init() {
        try {
            const response = await fetch('/api/v1/auth/session', {
                method: 'GET',
            });

            const result = await response.json();

            if (result !== null) {
                const user: IUser = {
                    id: result.id,
                    tenantId: result.tenant_id,
                    username: result.username,
                    status: result.status,
                    createdAt: result.created_at,
                    updatedAt: result.updated_at,
                    authenticatedAt: result.authenticated_at,
                };

                this.emit(user);
            }
        } catch (error) {
            this.emit(null);
            throw error;
        }
    }

    async login(username: string, password: string) {
        try {
            const payload = new URLSearchParams({
                username,
                password,
            });

            const response = await fetch('/api/v1/auth/login', {
                method: 'POST',
                body: payload,
            });

            const result = await response.json();

            const user: IUser = {
                id: result.id,
                tenantId: result.tenant_id,
                username: result.username,
                status: result.status,
                createdAt: result.created_at,
                updatedAt: result.updated_at,
                authenticatedAt: result.authenticated_at,
            };

            this.emit(user);
        } catch (error) {
            throw error;
        }
    }

    async logout() {
        try {
            const response = await fetch('/api/v1/auth/logout', {
                method: 'GET',
            });

            const result = await response.json();

            if (result !== null) {
                this.emit(null);
            }
        } catch (error) {
            throw error;
        }
    }

    getCurrentUser() {
        return this.currentUser;
    }
}

export const authService = new AuthService();

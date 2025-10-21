import { defineStore } from 'pinia';
import api from '../api/http';

export type UserRole = 'OWNER' | 'VET' | 'CLINIC_ADMIN';

export interface UserInfo {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  created_at: string;
}

interface AuthState {
  token: string | null;
  user: UserInfo | null;
  loading: boolean;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('pc_token'),
    user: null,
    loading: false,
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
  },
  actions: {
    async register(payload: { email: string; password: string; full_name: string; role: UserRole }) {
      await api.post('/api/auth/register', payload);
    },
    async login(payload: { email: string; password: string }) {
      this.loading = true;
      try {
        const { data } = await api.post('/api/auth/login', payload);
        this.token = data.access_token;
        localStorage.setItem('pc_token', this.token || '');
        await this.fetchMe();
      } finally {
        this.loading = false;
      }
    },
    async fetchMe() {
      if (!this.token) return;
      try {
        const { data } = await api.get<UserInfo>('/api/me');
        this.user = data;
      } catch (error) {
        this.logout();
        throw error;
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('pc_token');
    },
  },
});

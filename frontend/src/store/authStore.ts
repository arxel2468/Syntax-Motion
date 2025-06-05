import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { apiService } from '../api/api';
import { handleApiError } from '../utils/errorHandler';
import type { AuthResponse, LoginRequest, RegisterRequest, User } from '../types';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

interface AuthActions {
  login: (data: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
  checkAuth: () => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthState & AuthActions>()(
  persist(
    (set, get) => ({
      // State
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
      
      // Actions
      login: async (data: LoginRequest) => {
        set({ isLoading: true, error: null });
        try {
          const response = await apiService.login(data);
          localStorage.setItem('token', response.access_token);
          set({ isAuthenticated: true, isLoading: false });
        } catch (error) {
          console.error('Login error:', error);
          set({ 
            error: handleApiError(error), 
            isLoading: false 
          });
        }
      },
      
      register: async (data: RegisterRequest) => {
        set({ isLoading: true, error: null });
        try {
          const user = await apiService.register(data);
          const loginResponse = await apiService.login({
            username: data.username,
            password: data.password,
          });
          localStorage.setItem('token', loginResponse.access_token);
          set({ user, isAuthenticated: true, isLoading: false });
        } catch (error) {
          console.error('Registration error:', error);
          set({ 
            error: handleApiError(error), 
            isLoading: false 
          });
        }
      },
      
      logout: () => {
        localStorage.removeItem('token');
        set({ user: null, isAuthenticated: false });
      },
      
      checkAuth: () => {
        const token = localStorage.getItem('token');
        set({ isAuthenticated: !!token });
      },
      
      clearError: () => set({ error: null }),
    }),
    {
      name: 'auth-storage', // Name for the persisted state
      partialize: (state) => ({ isAuthenticated: state.isAuthenticated }), // Only persist authentication status
    }
  )
);

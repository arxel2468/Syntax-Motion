import { create } from 'zustand';
import { apiService } from '../api/api';
import type { AuthResponse, LoginRequest, RegisterRequest, User } from '../types';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  login: (data: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
  checkAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
  
  login: async (data: LoginRequest) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiService.login(data);
      localStorage.setItem('token', response.access_token);
      set({ isAuthenticated: true, isLoading: false });
    } catch (error: any) {
      console.error('Login error:', error);
      set({ 
        error: error.response?.data?.detail || 'Failed to login. Please check your credentials.', 
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
    } catch (error: any) {
      console.error('Registration error:', error);
      set({ 
        error: error.response?.data?.detail || 'Failed to register. Please try again.', 
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
})); 
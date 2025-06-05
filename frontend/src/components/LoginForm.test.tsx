import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import LoginForm from './LoginForm';

// Mock the hooks
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => vi.fn(),
    useLocation: () => ({ state: null }),
  };
});

vi.mock('../store/authStore', () => ({
  useAuthStore: () => ({
    login: vi.fn(),
    isLoading: false,
    error: null,
    isAuthenticated: false,
    clearError: vi.fn(),
  }),
}));

vi.mock('./Toast', () => ({
  useToast: () => ({
    showToast: vi.fn(),
  }),
}));

describe('LoginForm', () => {
  it('renders correctly', () => {
    render(
      <BrowserRouter>
        <LoginForm />
      </BrowserRouter>
    );
    
    expect(screen.getByText('Login to Your Account')).toBeInTheDocument();
    expect(screen.getByLabelText(/Username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Login/i })).toBeInTheDocument();
  });
  
  it('handles form input', () => {
    render(
      <BrowserRouter>
        <LoginForm />
      </BrowserRouter>
    );
    
    const usernameInput = screen.getByLabelText(/Username/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    
    expect(usernameInput).toHaveValue('testuser');
    expect(passwordInput).toHaveValue('password123');
  });
});

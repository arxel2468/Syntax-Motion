import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { ROUTES } from '../utils/routePaths';

type AuthWrapperProps = {
  children: React.ReactNode;
};

const AuthWrapper = ({ children }: AuthWrapperProps) => {
  const { isAuthenticated, checkAuth } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  
  useEffect(() => {
    checkAuth();
    
    // Redirect authenticated users away from auth pages
    if (isAuthenticated) {
      const isAuthPage = 
        location.pathname === ROUTES.LOGIN || 
        location.pathname === ROUTES.REGISTER || 
        location.pathname === ROUTES.HOME;
        
      if (isAuthPage) {
        navigate(ROUTES.DASHBOARD, { replace: true });
      }
    }
  }, [checkAuth, isAuthenticated, location.pathname, navigate]);

  return <>{children}</>;
};

export default AuthWrapper;

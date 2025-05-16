import { useEffect } from 'react';
import { useAuthStore } from './store/authStore';
import Navbar from './components/Navbar';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import ProjectList from './pages/ProjectList';
import CreateProject from './pages/CreateProject';
import ProjectDetail from './pages/ProjectDetail';
import SceneDetail from './pages/SceneDetail';
import './App.css';

function App() {
  const { isAuthenticated, checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
    
    // Redirect to dashboard if authenticated and on login/register page
    if (isAuthenticated) {
      const path = window.location.pathname;
      if (path === '/login' || path === '/register' || path === '/') {
        window.location.href = '/dashboard';
      }
    }
  }, [checkAuth, isAuthenticated]);

  // For simplicity in this MVP, we're using a very basic routing approach
  // In a full implementation, you would use a proper router like React Router
  const renderContent = () => {
    const path = window.location.pathname;

    if (!isAuthenticated) {
      if (path === '/register') {
        return (
          <div className="flex items-center justify-center min-h-screen bg-background p-4">
            <RegisterForm />
          </div>
        );
      }

  return (
        <div className="flex items-center justify-center min-h-screen bg-background p-4">
          <LoginForm />
        </div>
      );
    }

    // Simple routing for authenticated users
    if (path === '/dashboard' || path === '/') {
      return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
          <p className="mb-4">Welcome to Syntax Motion - AI-Powered Animated Video Generator!</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="card p-6">
              <h2 className="text-xl font-semibold mb-3">Create New Project</h2>
              <p className="text-gray-600 mb-4">Start a new animated video project from scratch.</p>
              <a href="/projects/new" className="btn btn-primary inline-block">
                New Project
              </a>
            </div>
            <div className="card p-6">
              <h2 className="text-xl font-semibold mb-3">My Projects</h2>
              <p className="text-gray-600 mb-4">View and manage your existing animation projects.</p>
              <a href="/projects" className="btn btn-outline inline-block">
                View Projects
              </a>
            </div>
          </div>
        </div>
      );
    }
    
    // Projects routes
    if (path === '/projects') {
      return <ProjectList />;
    }
    
    if (path === '/projects/new') {
      return <CreateProject />;
    }
    
    // Project detail route - example: /projects/123
    if (path.match(/^\/projects\/[a-zA-Z0-9-]+$/)) {
      return <ProjectDetail />;
    }
    
    // Scene detail route - example: /projects/123/scenes/456
    if (path.match(/^\/projects\/[a-zA-Z0-9-]+\/scenes\/[a-zA-Z0-9-]+$/)) {
      return <SceneDetail />;
    }

    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <a href="/dashboard" className="btn btn-primary mt-4 inline-block">
          Back to Dashboard
        </a>
      </div>
    );
  };

  return (
    <>
      <Navbar />
      <main>
        {renderContent()}
      </main>
    </>
  );
}

export default App;

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ToastProvider } from './components/Toast';
import Navbar from './components/Navbar';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import Dashboard from './pages/Dashboard';
import ProjectList from './pages/ProjectList';
import CreateProject from './pages/CreateProject';
import ProjectDetail from './pages/ProjectDetail';
import SceneDetail from './pages/SceneDetail';
import ProtectedRoute from './components/ProtectedRoute';
import AuthWrapper from './components/AuthWrapper';
import { ROUTES } from './utils/routePaths';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <ToastProvider>
        <AuthWrapper>
          <Navbar />
          <main>
            <Routes>
              {/* Public routes */}
              <Route path={ROUTES.LOGIN} element={<LoginForm />} />
              <Route path={ROUTES.REGISTER} element={<RegisterForm />} />
              
              {/* Protected routes */}
              <Route element={<ProtectedRoute />}>
                <Route path={ROUTES.DASHBOARD} element={<Dashboard />} />
                <Route path={ROUTES.PROJECTS} element={<ProjectList />} />
                <Route path={ROUTES.NEW_PROJECT} element={<CreateProject />} />
                <Route path="/projects/:projectId" element={<ProjectDetail />} />
                <Route path="/projects/:projectId/scenes/:sceneId" element={<SceneDetail />} />
              </Route>
              
              {/* Redirect home to dashboard or login */}
              <Route path={ROUTES.HOME} element={<Navigate to={ROUTES.DASHBOARD} replace />} />
              
              {/* 404 route */}
              <Route path="*" element={
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                  <h1 className="text-3xl font-bold text-gray-900 mb-6">Page Not Found</h1>
                  <p>The page you're looking for doesn't exist.</p>
                  <a href={ROUTES.DASHBOARD} className="btn btn-primary mt-4 inline-block">
                    Back to Dashboard
                  </a>
                </div>
              } />
            </Routes>
          </main>
        </AuthWrapper>
      </ToastProvider>
    </BrowserRouter>
  );
}

export default App;

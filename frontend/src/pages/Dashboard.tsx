import { Link } from 'react-router-dom';
import { ROUTES } from '../utils/routePaths';

const Dashboard = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
      <p className="mb-4">Welcome to Syntax Motion - AI-Powered Animated Video Generator!</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card p-6">
          <h2 className="text-xl font-semibold mb-3">Create New Project</h2>
          <p className="text-gray-600 mb-4">Start a new animated video project from scratch.</p>
          <Link to={ROUTES.NEW_PROJECT} className="btn btn-primary inline-block">
            New Project
          </Link>
        </div>
        <div className="card p-6">
          <h2 className="text-xl font-semibold mb-3">My Projects</h2>
          <p className="text-gray-600 mb-4">View and manage your existing animation projects.</p>
          <Link to={ROUTES.PROJECTS} className="btn btn-outline inline-block">
            View Projects
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

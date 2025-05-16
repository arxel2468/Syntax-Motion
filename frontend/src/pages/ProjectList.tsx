import { useEffect, useState } from 'react';
import { useProjectStore } from '../store/projectStore';
import ProjectCard from '../components/ProjectCard';

const ProjectList = () => {
  const { projects, fetchProjects, deleteProject, updateProject, isLoading, error } = useProjectStore();
  const [editMode, setEditMode] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  const handleEditClick = (id: string) => {
    const project = projects.find(p => p.id === id);
    if (project) {
      setEditTitle(project.title);
      setEditMode(id);
    }
  };

  const handleCancelEdit = () => {
    setEditMode(null);
    setEditTitle('');
  };

  const handleSaveEdit = async (id: string) => {
    if (!editTitle.trim()) return;
    
    try {
      await updateProject(id, editTitle);
      setEditMode(null);
      setEditTitle('');
    } catch (err) {
      console.error('Error updating project:', err);
    }
  };

  const handleDeleteProject = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this project? This action cannot be undone.')) {
      try {
        await deleteProject(id);
      } catch (err) {
        console.error('Error deleting project:', err);
      }
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center">
          <a 
            href="/dashboard" 
            className="text-gray-500 hover:text-gray-700 mr-2"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          </a>
          <h1 className="text-3xl font-bold text-gray-900">My Projects</h1>
        </div>
        <a href="/projects/new" className="btn btn-primary flex items-center">
          <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          New Project
        </a>
      </div>
      
      {error && (
        <div className="bg-red-50 text-red-500 p-3 rounded-md mb-4">
          {error}
        </div>
      )}
      
      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <svg className="animate-spin h-8 w-8 text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      ) : projects.length === 0 ? (
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <h2 className="text-xl font-medium text-gray-900 mb-2">No Projects Yet</h2>
          <p className="text-gray-600 mb-6">
            You haven't created any animation projects yet. Get started by creating your first project.
          </p>
          <a href="/projects/new" className="btn btn-primary inline-block">
            Create Your First Project
          </a>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map(project => (
            <div key={project.id} className={editMode === project.id ? "card p-5" : ""}>
              {editMode === project.id ? (
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-3">Edit Project</h3>
                  <input
                    type="text"
                    value={editTitle}
                    onChange={e => setEditTitle(e.target.value)}
                    className="input w-full mb-3"
                    placeholder="Project Title"
                  />
                  <div className="flex justify-end space-x-2">
                    <button
                      onClick={handleCancelEdit}
                      className="btn btn-outline"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={() => handleSaveEdit(project.id)}
                      className="btn btn-primary"
                    >
                      Save
                    </button>
                  </div>
                </div>
              ) : (
                <ProjectCard
                  project={project}
                  onEdit={handleEditClick}
                  onDelete={handleDeleteProject}
                />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProjectList; 
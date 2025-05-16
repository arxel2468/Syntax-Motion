import { useEffect, useState } from 'react';
import { useProjectStore } from '../store/projectStore';
import { SceneStatus } from '../types';
import SceneCard from '../components/SceneCard';

const ProjectDetail = () => {
  const { 
    currentProject, 
    fetchProject, 
    createScene, 
    updateScene, 
    deleteScene, 
    isLoading, 
    error 
  } = useProjectStore();
  
  const [prompt, setPrompt] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  
  // Get projectId from URL
  const projectId = window.location.pathname.split('/').pop() || '';
  
  useEffect(() => {
    if (projectId) {
      fetchProject(projectId);
    }
  }, [projectId, fetchProject]);

  // Poll for updates to scenes that are processing
  useEffect(() => {
    if (!currentProject) return;
    
    const hasProcessingScenes = currentProject.scenes.some(
      scene => scene.status === SceneStatus.PROCESSING
    );
    
    if (hasProcessingScenes) {
      const intervalId = setInterval(() => {
        fetchProject(projectId);
      }, 5000); // Poll every 5 seconds
      
      return () => clearInterval(intervalId);
    }
  }, [currentProject, projectId, fetchProject]);

  const handleCreateScene = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || !projectId) return;
    
    try {
      setIsCreating(true);
      const newScene = await createScene(projectId, prompt);
      setPrompt('');
      console.log('Created scene:', newScene);
      console.log('Scene project ID:', newScene.project_id);
      
      setTimeout(() => {
        fetchProject(projectId);
      }, 1000);
    } catch (error) {
      console.error('Error creating scene:', error);
    } finally {
      setIsCreating(false);
    }
  };

  const handleEditScene = (sceneId: string, newPrompt: string) => {
    if (!projectId) return;
    updateScene(projectId, sceneId, { prompt: newPrompt });
  };

  const handleDeleteScene = (sceneId: string) => {
    if (!projectId || !window.confirm('Are you sure you want to delete this scene?')) return;
    deleteScene(projectId, sceneId);
  };

  if (isLoading && !currentProject) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-center items-center h-64">
          <svg className="animate-spin h-8 w-8 text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      </div>
    );
  }

  if (!currentProject) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <h2 className="text-xl font-medium text-gray-900 mb-2">Project Not Found</h2>
          <p className="text-gray-600 mb-6">
            The project you're looking for doesn't exist or you don't have access to it.
          </p>
          <div className="flex space-x-2 justify-center">
            <a href="/projects" className="btn btn-primary inline-block">
              Back to Projects
            </a>
            <a href="/dashboard" className="btn btn-outline inline-block">
              Back to Dashboard
            </a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{currentProject.title}</h1>
          <p className="text-sm text-gray-500 mt-1">
            Created on {new Date(currentProject.created_at).toLocaleDateString()}
          </p>
        </div>
        <a href="/projects" className="btn btn-outline">
          Back to Projects
        </a>
      </div>
      
      {error && (
        <div className="bg-red-50 text-red-500 p-4 rounded-md mb-6">
          {error}
        </div>
      )}
      
      <div className="bg-white shadow-md rounded-lg mb-8">
        <div className="p-6">
          <h2 className="text-xl font-semibold mb-4">Add New Scene</h2>
          <form onSubmit={handleCreateScene}>
            <div className="mb-4">
              <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-1">
                Describe your animation
              </label>
              <textarea
                id="prompt"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="input w-full h-24"
                placeholder="Example: A ball bouncing on a surface, demonstrating gravity and elasticity"
                required
              />
            </div>
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isCreating || isLoading}
                className="btn btn-primary flex items-center"
              >
                {isCreating ? (
                  <>
                    <svg className="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Creating...
                  </>
                ) : (
                  <>Generate Animation</>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
      
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Scenes</h2>
      
      {currentProject.scenes.length === 0 ? (
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <h3 className="text-xl font-medium text-gray-900 mb-2">No Scenes Yet</h3>
          <p className="text-gray-600">
            Add your first scene by filling out the form above.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {currentProject.scenes
            .sort((a, b) => a.order - b.order)
            .map(scene => (
              <SceneCard
                key={scene.id}
                scene={scene}
                onEdit={handleEditScene}
                onDelete={handleDeleteScene}
              />
            ))}
        </div>
      )}
    </div>
  );
};

export default ProjectDetail; 
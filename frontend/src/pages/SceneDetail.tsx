import { useEffect, useState } from 'react';
import { useProjectStore } from '../store/projectStore';
import { SceneStatus } from '../types';

const SceneDetail = () => {
  const { currentScene, fetchScene, updateScene, isLoading, error } = useProjectStore();
  const [editMode, setEditMode] = useState(false);
  const [prompt, setPrompt] = useState('');
  
  // Get projectId and sceneId from URL path
  const pathParts = window.location.pathname.split('/');
  // Make sure we get the correct IDs by finding "projects" and "scenes" in the path
  const projectIndex = pathParts.findIndex(part => part === 'projects');
  const sceneIndex = pathParts.findIndex(part => part === 'scenes');
  
  let projectId = '';
  let sceneId = '';
  
  if (projectIndex !== -1 && projectIndex + 1 < pathParts.length) {
    projectId = pathParts[projectIndex + 1];
  }
  
  if (sceneIndex !== -1 && sceneIndex + 1 < pathParts.length) {
    sceneId = pathParts[sceneIndex + 1];
  }
  
  useEffect(() => {
    if (projectId && sceneId) {
      fetchScene(projectId, sceneId);
    }
  }, [projectId, sceneId, fetchScene]);
  
  useEffect(() => {
    if (currentScene) {
      setPrompt(currentScene.prompt);
    }
  }, [currentScene]);

  // Poll for updates if the scene is processing
  useEffect(() => {
    if (!currentScene || currentScene.status !== SceneStatus.PROCESSING) return;
    
    const intervalId = setInterval(() => {
      fetchScene(projectId, sceneId);
    }, 5000); // Poll every 5 seconds
    
    return () => clearInterval(intervalId);
  }, [currentScene, projectId, sceneId, fetchScene]);

  const handleEdit = () => {
    setEditMode(true);
  };

  const handleCancel = () => {
    setEditMode(false);
    if (currentScene) {
      setPrompt(currentScene.prompt);
    }
  };

  const handleSave = async () => {
    if (!currentScene || !prompt.trim()) return;
    
    try {
      await updateScene(projectId, sceneId, { prompt });
      setEditMode(false);
    } catch (err) {
      console.error('Error updating scene:', err);
    }
  };

  if (isLoading && !currentScene) {
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

  if (!currentScene) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <h2 className="text-xl font-medium text-gray-900 mb-2">Scene Not Found</h2>
          <p className="text-gray-600 mb-6">
            The scene you're looking for doesn't exist or you don't have access to it.
          </p>
          <div className="flex flex-col space-y-2 sm:flex-row sm:space-y-0 sm:space-x-2 justify-center">
            {projectId && (
              <a href={`/projects/${projectId}`} className="btn btn-primary inline-block">
                Back to Project
              </a>
            )}
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
        <h1 className="text-3xl font-bold text-gray-900">Scene Details</h1>
        <a href={`/projects/${projectId}`} className="btn btn-outline">
          Back to Project
        </a>
      </div>
      
      {error && (
        <div className="bg-red-50 text-red-500 p-4 rounded-md mb-6">
          {error}
        </div>
      )}
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <div className="bg-white shadow-md rounded-lg mb-6">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-xl font-semibold">Scene Information</h2>
                {!editMode && (
                  <button
                    onClick={handleEdit}
                    className="text-primary hover:text-primary-600 focus:outline-none"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                    </svg>
                  </button>
                )}
              </div>
              
              {editMode ? (
                <div>
                  <div className="mb-4">
                    <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-1">
                      Animation Prompt
                    </label>
                    <textarea
                      id="prompt"
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      className="input w-full h-32"
                      placeholder="Describe your animation"
                      required
                    />
                  </div>
                  <div className="flex justify-end space-x-2">
                    <button
                      onClick={handleCancel}
                      className="btn btn-outline"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={handleSave}
                      className="btn btn-primary"
                    >
                      Save & Regenerate
                    </button>
                  </div>
                </div>
              ) : (
                <div>
                  <div className="mb-4">
                    <h3 className="text-sm font-medium text-gray-500">Prompt</h3>
                    <p className="mt-1">{currentScene.prompt}</p>
                  </div>
                  
                  <div className="mb-4">
                    <h3 className="text-sm font-medium text-gray-500">Status</h3>
                    <div className="mt-1 flex items-center">
                      {currentScene.status === SceneStatus.PENDING && (
                        <span className="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full">
                          Pending
                        </span>
                      )}
                      {currentScene.status === SceneStatus.PROCESSING && (
                        <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full flex items-center">
                          <svg className="animate-spin h-3 w-3 mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Processing
                        </span>
                      )}
                      {currentScene.status === SceneStatus.COMPLETED && (
                        <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                          Completed
                        </span>
                      )}
                      {currentScene.status === SceneStatus.FAILED && (
                        <span className="px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">
                          Failed
                        </span>
                      )}
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-sm font-medium text-gray-500">Created At</h3>
                    <p className="mt-1">{new Date(currentScene.created_at).toLocaleString()}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
          
          {currentScene.status === SceneStatus.COMPLETED && currentScene.video_url && (
            <div className="bg-white shadow-md rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Animation Preview</h2>
              <video 
                className="w-full h-auto rounded-md" 
                controls 
                src={`http://localhost:8000${currentScene.video_url}`}
              />
              <div className="mt-4">
                <a 
                  href={`http://localhost:8000${currentScene.video_url}`}
                  download
                  className="btn btn-primary w-full"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Download Video
                </a>
              </div>
            </div>
          )}
        </div>
        
        {/* Generated Code Section */}
        {currentScene.code && (
          <div className="bg-white shadow-md rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Generated Manim Code</h2>
            {currentScene.status === SceneStatus.FAILED ? (
              <div className="bg-red-50 p-4 rounded-md mb-4">
                <p className="text-red-600 font-medium">Animation generation failed</p>
                <p className="text-red-500 text-sm mt-1">
                  There was an error generating or rendering the animation. 
                  The code below may contain syntax errors.
                </p>
              </div>
            ) : null}
            <pre className="bg-gray-50 p-4 rounded-md overflow-x-auto text-sm">
              <code>{currentScene.code}</code>
            </pre>
            {currentScene.status === SceneStatus.FAILED && (
              <div className="mt-4">
                <button 
                  onClick={() => updateScene(projectId, sceneId, { 
                    status: SceneStatus.PENDING,
                    prompt: currentScene.prompt 
                  })}
                  className="btn btn-primary w-full"
                >
                  Retry Animation Generation
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SceneDetail; 
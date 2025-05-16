import { useState } from 'react';
import type { Scene } from '../types';
import { SceneStatus } from '../types';

interface SceneCardProps {
  scene: Scene;
  onEdit: (id: string, prompt: string) => void;
  onDelete: (id: string) => void;
}

const SceneCard = ({ scene, onEdit, onDelete }: SceneCardProps) => {
  const [isEditing, setIsEditing] = useState(false);
  const [prompt, setPrompt] = useState(scene.prompt);
  
  const handleSave = () => {
    if (!prompt.trim()) return;
    onEdit(scene.id, prompt);
    setIsEditing(false);
  };
  
  const handleCancel = () => {
    setPrompt(scene.prompt);
    setIsEditing(false);
  };
  
  const statusLabel = {
    [SceneStatus.PENDING]: 'Pending',
    [SceneStatus.PROCESSING]: 'Processing',
    [SceneStatus.COMPLETED]: 'Completed',
    [SceneStatus.FAILED]: 'Failed'
  };
  
  const statusColors = {
    [SceneStatus.PENDING]: 'bg-yellow-100 text-yellow-800',
    [SceneStatus.PROCESSING]: 'bg-blue-100 text-blue-800',
    [SceneStatus.COMPLETED]: 'bg-green-100 text-green-800',
    [SceneStatus.FAILED]: 'bg-red-100 text-red-800'
  };

  return (
    <div className="card hover:shadow-lg transition-shadow overflow-hidden">
      <div className="p-5">
        <div className="flex justify-between items-start mb-3">
          <div className="flex items-center">
            <span className={`px-2 py-1 text-xs font-medium ${statusColors[scene.status]} rounded-full mr-2`}>
              {statusLabel[scene.status]}
            </span>
            <span className="text-sm text-gray-500">Scene #{scene.order + 1}</span>
          </div>
          <div className="flex space-x-2">
            {!isEditing && scene.status !== SceneStatus.PROCESSING && (
              <>
                <button
                  onClick={() => setIsEditing(true)}
                  className="text-gray-500 hover:text-primary focus:outline-none"
                  aria-label="Edit scene"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                  </svg>
                </button>
                <button
                  onClick={() => onDelete(scene.id)}
                  className="text-gray-500 hover:text-red-500 focus:outline-none"
                  aria-label="Delete scene"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </button>
              </>
            )}
          </div>
        </div>
        
        {isEditing ? (
          <div>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="input w-full h-32 mb-3"
              placeholder="Describe your animation"
            />
            <div className="flex justify-end space-x-2">
              <button
                onClick={handleCancel}
                className="btn btn-outline btn-sm"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="btn btn-primary btn-sm"
              >
                Save
              </button>
            </div>
          </div>
        ) : (
          <p className="text-gray-700 mb-4 line-clamp-3">{scene.prompt}</p>
        )}
        
        {scene.status === SceneStatus.COMPLETED && scene.video_url && (
          <div className="mt-3">
            <video 
              className="w-full h-auto rounded-md" 
              controls 
              src={`http://localhost:8000${scene.video_url}`}
            />
          </div>
        )}
        
        {scene.status === SceneStatus.PROCESSING && (
          <div className="flex justify-center items-center mt-3 bg-gray-50 rounded-md p-4">
            <svg className="animate-spin h-6 w-6 text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span className="ml-2 text-sm text-gray-600">Generating animation...</span>
          </div>
        )}
        
        {scene.status === SceneStatus.FAILED && (
          <div className="mt-3 bg-red-50 text-red-500 p-3 rounded-md text-sm">
            Failed to generate animation. Please try again.
          </div>
        )}
      </div>
      
      <div className="px-5 py-3 bg-gray-50 border-t border-gray-100">
        <a 
          href={`/projects/${scene.project_id}/scenes/${scene.id}`}
          className="text-primary hover:text-primary-600 text-sm font-medium flex items-center"
          onClick={(e) => {
            if (!scene.project_id || scene.project_id === 'undefined') {
              e.preventDefault();
              console.error('Invalid project ID:', scene.project_id);
              alert('Error: Invalid project ID. Please try again later.');
            }
          }}
        >
          View Details
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </a>
      </div>
    </div>
  );
};

export default SceneCard; 
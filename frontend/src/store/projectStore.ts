import { create } from 'zustand';
import { apiService } from '../api/api';
import { handleApiError } from '../utils/errorHandler';
import type { Project, ProjectWithScenes, Scene, SceneDetail } from '../types';

interface ProjectState {
  projects: Project[];
  currentProject: ProjectWithScenes | null;
  currentScene: SceneDetail | null;
  isLoading: boolean;
  error: string | null;
}

interface ProjectActions {
  fetchProjects: () => Promise<void>;
  fetchProject: (id: string) => Promise<void>;
  fetchScene: (projectId: string, sceneId: string) => Promise<void>;
  createProject: (title: string) => Promise<Project>;
  updateProject: (id: string, title: string) => Promise<Project>;
  deleteProject: (id: string) => Promise<void>;
  createScene: (projectId: string, prompt: string, order?: number) => Promise<Scene>;
  updateScene: (projectId: string, sceneId: string, data: Partial<Scene>) => Promise<Scene>;
  deleteScene: (projectId: string, sceneId: string) => Promise<void>;
  clearError: () => void;
}

interface ProjectSelectors {
  getProjectById: (id: string) => Project | undefined;
}

type ProjectStore = ProjectState & ProjectActions & ProjectSelectors;

export const useProjectStore = create<ProjectStore>((set, get) => ({
  // State
  projects: [],
  currentProject: null,
  currentScene: null,
  isLoading: false,
  error: null,
  
  // Selectors
  getProjectById: (id: string) => get().projects.find(p => p.id === id),
  
  // Actions
  fetchProjects: async () => {
    set({ isLoading: true, error: null });
    try {
      const projects = await apiService.getProjects();
      set({ projects, isLoading: false });
    } catch (error) {
      console.error('Error fetching projects:', error);
      set({ 
        error: handleApiError(error), 
        isLoading: false 
      });
    }
  },
  
  fetchProject: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      const project = await apiService.getProject(id);
      set({ currentProject: project, isLoading: false });
    } catch (error) {
      console.error('Error fetching project:', error);
      set({ 
        error: handleApiError(error), 
        isLoading: false 
      });
    }
  },
  
  fetchScene: async (projectId: string, sceneId: string) => {
    set({ isLoading: true, error: null });
    try {
      const scene = await apiService.getScene(projectId, sceneId);
      set({ currentScene: scene, isLoading: false });
    } catch (error) {
      console.error('Error fetching scene:', error);
      set({ 
        error: handleApiError(error), 
        isLoading: false 
      });
    }
  },
  
  createProject: async (title: string) => {
    set({ isLoading: true, error: null });
    try {
      const project = await apiService.createProject(title);
      set(state => ({ 
        projects: [...state.projects, project],
        isLoading: false 
      }));
      return project;
    } catch (error) {
      console.error('Error creating project:', error);
      set({ 
        error: handleApiError(error), 
        isLoading: false 
      });
      throw error;
    }
  },
  
  updateProject: async (id: string, title: string) => {
    set({ isLoading: true, error: null });
    try {
      const updatedProject = await apiService.updateProject(id, title);
      set(state => ({
        projects: state.projects.map(p => p.id === id ? updatedProject : p),
        currentProject: state.currentProject?.id === id 
          ? { ...state.currentProject, ...updatedProject } 
          : state.currentProject,
        isLoading: false
      }));
      return updatedProject;
    } catch (error) {
      console.error('Error updating project:', error);
      set({ 
        error: handleApiError(error), 
        isLoading: false 
      });
      throw error;
    }
  },
  
  deleteProject: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      await apiService.deleteProject(id);
      set(state => ({
        projects: state.projects.filter(p => p.id !== id),
        currentProject: state.currentProject?.id === id ? null : state.currentProject,
        isLoading: false
      }));
    } catch (error) {
      console.error('Error deleting project:', error);
      set({ 
        error: handleApiError(error), 
        isLoading: false 
      });
      throw error;
    }
  },
  
  createScene: async (projectId: string, prompt: string, order = 0) => {
    set({ isLoading: true, error: null });
    try {
      const scene = await apiService.createScene(projectId, prompt, order);
      set(state => {
        if (state.currentProject?.id === projectId) {
          return {
            currentProject: {
              ...state.currentProject,
              scenes: [...(state.currentProject.scenes || []), scene]
            },
            isLoading: false
          };
        }
        return { isLoading: false };
      });
      return scene;
    } catch (error) {
      console.error('Error creating scene:', error);
      set({ 
        error: handleApiError(error), 
        isLoading: false 
      });
      throw error;
    }
  },
  
  updateScene: async (projectId: string, sceneId: string, data: Partial<Scene>) => {
    set({ isLoading: true, error: null });
    try {
      const updatedScene = await apiService.updateScene(projectId, sceneId, data);
      set(state => {
        if (state.currentProject?.id === projectId) {
          return {
            currentProject: {
              ...state.currentProject,
              scenes: state.currentProject.scenes.map(s => 
                s.id === sceneId ? updatedScene : s
              )
            },
            currentScene: state.currentScene?.id === sceneId 
              ? { ...state.currentScene, ...updatedScene } 
              : state.currentScene,
            isLoading: false
          };
        }
        return { 
          currentScene: state.currentScene?.id === sceneId 
            ? { ...state.currentScene, ...updatedScene } 
            : state.currentScene,
          isLoading: false 
        };
      });
      return updatedScene;
    } catch (error) {
      console.error('Error updating scene:', error);
      set({ 
        error: handleApiError(error), 
        isLoading: false 
      });
      throw error;
    }
  },
  
  deleteScene: async (projectId: string, sceneId: string) => {
    set({ isLoading: true, error: null });
    try {
      await apiService.deleteScene(projectId, sceneId);
      set(state => {
        if (state.currentProject?.id === projectId) {
          return {
            currentProject: {
              ...state.currentProject,
              scenes: state.currentProject.scenes.filter(s => s.id !== sceneId)
            },
            currentScene: state.currentScene?.id === sceneId ? null : state.currentScene,
            isLoading: false
          };
        }
        return { 
          currentScene: state.currentScene?.id === sceneId ? null : state.currentScene,
          isLoading: false 
        };
      });
    } catch (error) {
      console.error('Error deleting scene:', error);
      set({ 
        error: handleApiError(error), 
        isLoading: false 
      });
      throw error;
    }
  },
  
  clearError: () => set({ error: null }),
}));

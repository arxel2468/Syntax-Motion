import axios, { AxiosInstance } from 'axios';
import type { 
  AuthResponse, 
  LoginRequest, 
  Project, 
  ProjectWithScenes, 
  RegisterRequest, 
  Scene, 
  SceneDetail, 
  User 
} from '../types/index';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiService {
  private api: AxiosInstance;
  
  constructor() {
    this.api = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    // Add interceptor to add authorization header
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );
  }
  
  // Auth endpoints
  async login(data: LoginRequest): Promise<AuthResponse> {
    const formData = new FormData();
    formData.append('username', data.username);
    formData.append('password', data.password);
    
    const response = await this.api.post<AuthResponse>('/auth/token', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
  
  async register(data: RegisterRequest): Promise<User> {
    const response = await this.api.post<User>('/auth/register', data);
    return response.data;
  }
  
  // Projects endpoints
  async getProjects(): Promise<Project[]> {
    const response = await this.api.get<Project[]>('/projects');
    return response.data;
  }
  
  async getProject(id: string): Promise<ProjectWithScenes> {
    const response = await this.api.get<ProjectWithScenes>(`/projects/${id}`);
    return response.data;
  }
  
  async createProject(title: string): Promise<Project> {
    const response = await this.api.post<Project>('/projects', { title });
    return response.data;
  }
  
  async updateProject(id: string, title: string): Promise<Project> {
    const response = await this.api.put<Project>(`/projects/${id}`, { title });
    return response.data;
  }
  
  async deleteProject(id: string): Promise<void> {
    await this.api.delete(`/projects/${id}`);
  }
  
  // Scenes endpoints
  async getScenes(projectId: string): Promise<Scene[]> {
    const response = await this.api.get<Scene[]>(`/projects/${projectId}/scenes`);
    return response.data;
  }
  
  async getScene(projectId: string, sceneId: string): Promise<SceneDetail> {
    const response = await this.api.get<SceneDetail>(`/projects/${projectId}/scenes/${sceneId}`);
    return response.data;
  }
  
  async createScene(projectId: string, prompt: string, order: number = 0): Promise<Scene> {
    const response = await this.api.post<Scene>(`/projects/${projectId}/scenes`, { prompt, order });
    return response.data;
  }
  
  async updateScene(projectId: string, sceneId: string, data: Partial<Scene>): Promise<Scene> {
    const response = await this.api.put<Scene>(`/projects/${projectId}/scenes/${sceneId}`, data);
    return response.data;
  }
  
  async deleteScene(projectId: string, sceneId: string): Promise<void> {
    await this.api.delete(`/projects/${projectId}/scenes/${sceneId}`);
  }
  
  async refinePrompt(projectTitle: string, prompt: string): Promise<string> {
    const response = await this.api.post<{ refined_prompt: string }>(
      '/ai/refine-prompt',
      { project_title: projectTitle, prompt }
    );
    return response.data.refined_prompt;
  }
}

export const apiService = new ApiService(); 
export enum SceneStatus {
  PENDING = "pending",
  PROCESSING = "processing",
  COMPLETED = "completed",
  FAILED = "failed",
}

export interface User {
  id: string;
  username: string;
  email: string;
}

export interface Project {
  id: string;
  title: string;
  user_id: string;
  created_at: string;
}

export interface ProjectWithScenes extends Project {
  scenes: Scene[];
}

export interface Scene {
  id: string;
  project_id: string;
  prompt: string;
  order: number;
  status: SceneStatus;
  video_url?: string;
  created_at: string;
}

export interface SceneDetail extends Scene {
  code?: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface ApiError {
  detail: string;
} 
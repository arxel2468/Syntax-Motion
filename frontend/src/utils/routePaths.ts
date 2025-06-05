// Centralized route definitions
export const ROUTES = {
    HOME: '/',
    LOGIN: '/login',
    REGISTER: '/register',
    DASHBOARD: '/dashboard',
    PROJECTS: '/projects',
    NEW_PROJECT: '/projects/new',
    PROJECT_DETAIL: (id: string) => `/projects/${id}`,
    SCENE_DETAIL: (projectId: string, sceneId: string) => `/projects/${projectId}/scenes/${sceneId}`,
  };
  
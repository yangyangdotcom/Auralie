import axios from 'axios';
import { Profile, SimulationResult, SimulationSummary, CreateProfileRequest } from '../types';

// Get API URL from environment or use default
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API] Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      console.error('[API] Request timeout');
    } else if (error.response) {
      console.error('[API] Error response:', error.response.status, error.response.data);
    } else if (error.request) {
      console.error('[API] No response received');
    } else {
      console.error('[API] Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// Profile endpoints
export const getProfiles = () =>
  api.get<Profile[]>('/api/profiles');

export const getProfile = (id: string) =>
  api.get<Profile>(`/api/profiles/${id}`);

export const createProfile = (data: CreateProfileRequest) =>
  api.post<Profile>('/api/profiles', data);

// Simulation endpoints
export const getSimulations = () =>
  api.get<SimulationSummary[]>('/api/simulations');

export const getSimulation = (id: string) =>
  api.get<SimulationResult>(`/api/simulations/${id}`);

export const runSimulation = (profile1_id: string, profile2_id: string) =>
  api.post<{ simulation_id: string; status: string }>('/api/simulations', {
    profile1_id,
    profile2_id,
  });

export const deleteSimulation = (id: string) =>
  api.delete(`/api/simulations/${id}`);

export default api;

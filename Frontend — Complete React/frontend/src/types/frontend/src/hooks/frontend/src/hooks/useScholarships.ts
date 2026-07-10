import { useQuery, useMutation } from '@tanstack/react-query';
import axios from 'axios';
import { Scholarship, ScholarshipMatch, ScholarshipFilters } from '../types/scholarship';
import { getAuthHeaders } from './useAuth';

const API_BASE = import.meta.env.VITE_API_URL || 'https://your-backend.vercel.app/api/v1';

const api = axios.create({ baseURL: API_BASE });

api.interceptors.request.use((config) => {
  const headers = getAuthHeaders();
  Object.assign(config.headers, headers);
  return config;
});

export const useScholarships = (filters: ScholarshipFilters = {}) => {
  return useQuery({
    queryKey: ['scholarships', filters],
    queryFn: async () => {
      const { data } = await api.get('/scholarships', { params: filters });
      return data as Scholarship[];
    },
  });
};

export const useScholarshipMatches = (topK = 50) => {
  return useQuery({
    queryKey: ['scholarship-matches', topK],
    queryFn: async () => {
      const { data } = await api.get('/scholarships/match', { params: { top_k: topK } });
      return data as ScholarshipMatch[];
    },
  });
};

export const useSeedDemoScholarships = () => {
  return useMutation({
    mutationFn: async () => {
      const { data } = await api.post('/scholarships/demo-seed');
      return data as Scholarship[];
    },
  });
};

import { useQuery, useMutation } from '@tanstack/react-query'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({ baseURL: API_BASE })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('knownet-auth')
  if (token) {
    try {
      const parsed = JSON.parse(token)
      if (parsed.state?.accessToken) {
        config.headers.Authorization = `Bearer ${parsed.state.accessToken}`
      }
    } catch {}
  }
  return config
})

export interface Scholarship {
  id: number
  title: string
  provider: string | null
  source_url: string
  deadline: string | null
  amount: string | null
  eligibility_raw: string | null
  field_tags: string[]
  country_scope: string[]
  education_levels: string[]
  is_active: boolean
  last_verified_at: string
  created_at: string
  updated_at: string
}

export interface ScholarshipMatch extends Scholarship {
  match_score: number
  semantic_score: number
  rule_score: number
  urgency_score: number
}

export interface ScholarshipFilters {
  search?: string
  field?: string
  country?: string
  education_level?: string
  active_only?: boolean
  sort_by?: 'deadline' | 'created_at' | 'relevance'
  page?: number
  page_size?: number
}

export const useScholarships = (filters: ScholarshipFilters = {}) => {
  return useQuery({
    queryKey: ['scholarships', filters],
    queryFn: async () => {
      const { data } = await api.get('/scholarships', { params: filters })
      return data as Scholarship[]
    },
  })
}

export const useScholarshipMatches = (topK = 50) => {
  return useQuery({
    queryKey: ['scholarship-matches', topK],
    queryFn: async () => {
      const { data } = await api.get('/scholarships/match', { params: { top_k: topK } })
      return data as ScholarshipMatch[]
    },
  })
}

export const useSeedDemoScholarships = () => {
  return useMutation({
    mutationFn: async () => {
      const { data } = await api.post('/scholarships/demo-seed')
      return data as Scholarship[]
    },
  })
}

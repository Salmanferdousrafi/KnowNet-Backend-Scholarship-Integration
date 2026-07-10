export interface User {
  id: number
  email: string
  full_name: string | null
  field_of_study: string | null
  country: string | null
  education_level: string | null
  bio: string | null
  is_active: boolean
  is_admin: boolean
  created_at: string
  updated_at: string
}

export interface Project {
  id: number
  title: string
  description: string | null
  is_public: boolean
  owner_id: number
  created_at: string
  updated_at: string
}

export interface KnowledgeEntry {
  id: number
  title: string
  content: string
  source_url: string | null
  tags: string[]
  is_public: boolean
  owner_id: number
  project_id: number | null
  created_at: string
  updated_at: string
}

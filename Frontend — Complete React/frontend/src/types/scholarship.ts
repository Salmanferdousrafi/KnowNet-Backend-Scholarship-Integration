export interface Scholarship {
  id: number;
  title: string;
  provider: string | null;
  source_url: string;
  deadline: string | null;
  amount: string | null;
  eligibility_raw: string | null;
  field_tags: string[];
  country_scope: string[];
  education_levels: string[];
  is_active: boolean;
  last_verified_at: string;
  created_at: string;
  updated_at: string;
  source_feed: string | null;
  external_id: string | null;
}

export interface ScholarshipMatch extends Scholarship {
  match_score: number;
  semantic_score: number;
  rule_score: number;
  urgency_score: number;
}

export interface ScholarshipFilters {
  search?: string;
  field?: string;
  country?: string;
  education_level?: string;
  active_only?: boolean;
  sort_by?: 'deadline' | 'created_at' | 'relevance';
  page?: number;
  page_size?: number;
}

"""
Scholarship Pydantic schemas.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ScholarshipBase(BaseModel):
    title: str
    provider: Optional[str] = None
    source_url: str
    deadline: Optional[datetime] = None
    amount: Optional[str] = None
    eligibility_raw: Optional[str] = None
    field_tags: Optional[List[str]] = None
    country_scope: Optional[List[str]] = None
    education_levels: Optional[List[str]] = None
    is_active: bool = True

class ScholarshipCreate(ScholarshipBase):
    external_id: Optional[str] = None
    source_feed: Optional[str] = None

class ScholarshipUpdate(BaseModel):
    title: Optional[str] = None
    provider: Optional[str] = None
    source_url: Optional[str] = None
    deadline: Optional[datetime] = None
    amount: Optional[str] = None
    eligibility_raw: Optional[str] = None
    field_tags: Optional[List[str]] = None
    country_scope: Optional[List[str]] = None
    education_levels: Optional[List[str]] = None
    is_active: Optional[bool] = None

class ScholarshipOut(ScholarshipBase):
    id: int
    last_verified_at: datetime
    created_at: datetime
    updated_at: datetime
    source_feed: Optional[str] = None
    external_id: Optional[str] = None

    class Config:
        from_attributes = True

class ScholarshipMatchOut(ScholarshipOut):
    match_score: float
    semantic_score: float
    rule_score: float
    urgency_score: float

class ScholarshipListParams(BaseModel):
    search: Optional[str] = None
    field: Optional[str] = None
    country: Optional[str] = None
    education_level: Optional[str] = None
    active_only: bool = True
    sort_by: str = "deadline"  # deadline, created_at, relevance
    page: int = 1
    page_size: int = 20

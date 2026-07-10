"""
Knowledge Pydantic schemas.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class KnowledgeBase(BaseModel):
    title: str
    content: str
    source_url: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: bool = False

class KnowledgeCreate(KnowledgeBase):
    project_id: Optional[int] = None

class KnowledgeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    source_url: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: Optional[bool] = None

class KnowledgeOut(KnowledgeBase):
    id: int
    owner_id: int
    project_id: Optional[int] = None
    embedding: Optional[List[float]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class KnowledgeSearchQuery(BaseModel):
    query: str
    top_k: int = 10
    project_id: Optional[int] = None

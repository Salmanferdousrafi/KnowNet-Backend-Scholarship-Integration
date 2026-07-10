"""
User Pydantic schemas.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    field_of_study: Optional[str] = None
    country: Optional[str] = None
    education_level: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    field_of_study: Optional[str] = None
    country: Optional[str] = None
    education_level: Optional[str] = None
    bio: Optional[str] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    bio_embedding: Optional[List[float]] = None

    class Config:
        from_attributes = True

class UserProfile(UserInDB):
    pass

class UserPublic(BaseModel):
    id: int
    full_name: Optional[str] = None
    field_of_study: Optional[str] = None

    class Config:
        from_attributes = True

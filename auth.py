"""
Auth-related Pydantic schemas.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds

class RefreshRequest(BaseModel):
    refresh_token: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    field_of_study: Optional[str] = None
    country: Optional[str] = None
    education_level: Optional[str] = None

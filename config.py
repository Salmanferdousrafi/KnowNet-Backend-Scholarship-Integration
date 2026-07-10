"""
App configuration. All secrets MUST come from environment variables.
App refuses to boot if JWT_SECRET or DATABASE_URL is missing.
"""
import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str

    # Security
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Claude / AI
    claude_api_key: str
    claude_model: str = "claude-3-5-sonnet-20241022"

    # App
    app_name: str = "KnowNet X"
    debug: bool = False
    environment: str = "production"

    # Rate Limiting
    rate_limit_login: str = "5/minute"
    rate_limit_register: str = "3/minute"

    # Scholarship Sources (comma-separated URLs/feed endpoints)
    scholarship_sources: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    settings = Settings()

    # Hard fail on missing critical secrets — no silent insecure fallback
    if not settings.database_url or settings.database_url.strip() == "":
        raise RuntimeError("FATAL: DATABASE_URL environment variable is required. Set it before starting the app.")

    if not settings.jwt_secret or settings.jwt_secret.strip() == "":
        raise RuntimeError("FATAL: JWT_SECRET environment variable is required. Set it before starting the app.")

    if not settings.claude_api_key or settings.claude_api_key.strip() == "":
        raise RuntimeError("FATAL: CLAUDE_API_KEY environment variable is required. Set it before starting the app.")

    # Minimum secret length check
    if len(settings.jwt_secret) < 32:
        raise RuntimeError("FATAL: JWT_SECRET must be at least 32 characters long.")

    return settings

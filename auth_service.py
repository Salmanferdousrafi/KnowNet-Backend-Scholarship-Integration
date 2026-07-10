"""
Auth service: login, token refresh, logout (revocation).
"""
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    hashlib,
)
from app.core.config import get_settings

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def issue_token_pair(db: Session, user: User) -> Tuple[str, str, int]:
    """Returns (access_token, refresh_token_raw, expires_in_seconds)."""
    settings = get_settings()
    access_token = create_access_token({"sub": user.email, "user_id": user.id})

    raw_refresh, token_hash = create_refresh_token({"sub": user.email, "user_id": user.id})

    # Store hashed refresh token in DB for revocation
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    db_token = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
    )
    db.add(db_token)
    db.commit()

    return access_token, raw_refresh, settings.access_token_expire_minutes * 60

def refresh_access_token(db: Session, raw_refresh_token: str) -> Tuple[str, str, int]:
    """Rotate refresh token: validate old, issue new pair."""
    from app.core.security import decode_token

    try:
        payload = decode_token(raw_refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    # Check hash against DB and ensure not revoked
    token_hash = hashlib.sha256(raw_refresh_token.encode()).hexdigest()
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash,
        RefreshToken.is_revoked == False,
        RefreshToken.expires_at > datetime.now(timezone.utc)
    ).first()

    if not db_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token invalid or revoked")

    # Revoke old token (single-use rotation)
    db_token.is_revoked = True
    db.commit()

    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User inactive")

    return issue_token_pair(db, user)

def revoke_refresh_token(db: Session, raw_refresh_token: str) -> bool:
    """Logout: revoke the refresh token server-side."""
    token_hash = hashlib.sha256(raw_refresh_token.encode()).hexdigest()
    db_token = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    if db_token:
        db_token.is_revoked = True
        db.commit()
        return True
    return False

def revoke_all_user_tokens(db: Session, user_id: int) -> int:
    """Revoke all refresh tokens for a user (e.g., password change, admin action)."""
    count = db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.is_revoked == False
    ).update({"is_revoked": True})
    db.commit()
    return count

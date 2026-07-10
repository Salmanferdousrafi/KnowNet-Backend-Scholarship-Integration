"""
User router: profile, update, me.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_active_user
from app.schemas.user import UserInDB, UserUpdate, UserProfile
from app.services.user_service import update_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserProfile)
async def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    return current_user

@router.patch("/me", response_model=UserProfile)
async def update_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    updated = update_user(db, current_user, user_update)
    return updated

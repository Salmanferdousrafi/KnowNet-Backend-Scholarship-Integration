"""
Admin-only endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, require_admin
from app.schemas.user import UserInDB
from app.scheduler.collector import run_collection_cycle

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/scholarships/trigger-collection")
async def trigger_scholarship_collection(
    db: Session = Depends(get_db),
    admin_user: UserInDB = Depends(require_admin),
):
    """Manually trigger the scholarship collection cycle. Admin only."""
    try:
        count = await run_collection_cycle(db)
        return {
            "detail": f"Collection cycle completed. {count} scholarships processed.",
            "processed": count,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Collection failed: {str(e)}")

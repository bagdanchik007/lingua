from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.leaderboard_service import xp_leaderboard

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/xp")
def get_xp_leaderboard(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return {"items": xp_leaderboard(db, limit)}

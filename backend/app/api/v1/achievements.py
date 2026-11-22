from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.achievement import AchievementRead, UserAchievementRead
from app.services.achievement_service import (
    list_achievements,
    list_user_achievements,
    evaluate_achievements,
    ensure_default_achievements,
)

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("/", response_model=list[AchievementRead])
def get_all_achievements(db: Session = Depends(get_db)):
    ensure_default_achievements(db)
    return list_achievements(db)


@router.get("/me", response_model=list[UserAchievementRead])
def get_my_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_user_achievements(db, current_user.id)


@router.post("/evaluate")
def evaluate_my_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    codes = evaluate_achievements(db, current_user.id)
    return {"newly_unlocked": codes}

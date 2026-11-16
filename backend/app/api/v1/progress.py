from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.progress import ExerciseSubmit, ExerciseResultRead, UserStats, UserProgressRead
from app.services.progress_service import submit_exercise, get_user_stats
from app.models.progress import UserProgress
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/progress", tags=["progress"])


@router.post("/exercise", response_model=ExerciseResultRead)
def submit_exercise_result(
    data: ExerciseSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return submit_exercise(db, current_user.id, data)


@router.get("/stats", response_model=UserStats)
def read_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_stats(db, current_user.id)


@router.get("/me", response_model=list[UserProgressRead])
def read_my_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(UserProgress).filter(UserProgress.user_id == current_user.id).all()

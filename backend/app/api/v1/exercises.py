from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.exercise import ExerciseCreate, ExerciseRead, ExerciseAnswer, ExerciseCheckResult
from app.services.exercise_service import create_exercise, list_exercises, check_answer
from app.services.activity_service import record_study
from app.services.streak_service import update_streak

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/", response_model=list[ExerciseRead])
def get_exercises(
    language_id: int | None = None,
    level_id: int | None = None,
    grammar_topic_id: int | None = None,
    exercise_type: str | None = None,
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    return list_exercises(db, language_id, level_id, grammar_topic_id, exercise_type, limit)


@router.post("/", response_model=ExerciseRead)
def add_exercise(
    data: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_exercise(db, data)


@router.post("/check", response_model=ExerciseCheckResult)
def submit_answer(
    payload: ExerciseAnswer,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = check_answer(db, current_user.id, payload)
    record_study(
        db,
        current_user,
        minutes=1,
        exercises_done=1,
        exercises_correct=1 if result.is_correct else 0,
        xp=result.xp_gained,
    )
    update_streak(db, current_user.id)
    return result

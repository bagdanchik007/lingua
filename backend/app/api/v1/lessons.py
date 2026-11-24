from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.lesson import Lesson
from app.services.lesson_service import list_lessons, get_lesson, update_lesson_progress

router = APIRouter(prefix="/lessons", tags=["lessons"])


class LessonRead(BaseModel):
    id: int
    language_id: int
    level_id: int | None
    title: str
    slug: str
    description: str | None
    order: int
    estimated_minutes: int

    model_config = {"from_attributes": True}


class LessonProgressUpdate(BaseModel):
    progress_percent: int = Field(ge=0, le=100)
    status: str | None = None


@router.get("/", response_model=list[LessonRead])
def get_lessons(
    language_id: int | None = None,
    level_id: int | None = None,
    db: Session = Depends(get_db),
):
    return list_lessons(db, language_id, level_id)


@router.get("/{lesson_id}", response_model=LessonRead)
def get_one_lesson(lesson_id: int, db: Session = Depends(get_db)):
    return get_lesson(db, lesson_id)


@router.post("/{lesson_id}/progress")
def set_progress(
    lesson_id: int,
    data: LessonProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = update_lesson_progress(
        db, current_user.id, lesson_id, data.progress_percent, data.status
    )
    return {
        "lesson_id": row.lesson_id,
        "status": row.status,
        "progress_percent": row.progress_percent,
    }

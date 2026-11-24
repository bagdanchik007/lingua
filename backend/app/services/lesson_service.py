from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.lesson import Lesson, UserLessonProgress
from app.utils.exceptions import NotFoundError


def list_lessons(db: Session, language_id: int | None = None, level_id: int | None = None):
    q = db.query(Lesson).filter(Lesson.is_active == True)
    if language_id:
        q = q.filter(Lesson.language_id == language_id)
    if level_id:
        q = q.filter(Lesson.level_id == level_id)
    return q.order_by(Lesson.order).all()


def get_lesson(db: Session, lesson_id: int) -> Lesson:
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.is_active == True).first()
    if not lesson:
        raise NotFoundError("Lesson not found")
    return lesson


def update_lesson_progress(
    db: Session,
    user_id: int,
    lesson_id: int,
    progress_percent: int,
    status: str | None = None,
) -> UserLessonProgress:
    get_lesson(db, lesson_id)
    row = (
        db.query(UserLessonProgress)
        .filter(UserLessonProgress.user_id == user_id, UserLessonProgress.lesson_id == lesson_id)
        .first()
    )
    if not row:
        row = UserLessonProgress(user_id=user_id, lesson_id=lesson_id)
        db.add(row)

    row.progress_percent = max(0, min(100, progress_percent))
    if status:
        row.status = status
    elif row.progress_percent >= 100:
        row.status = "completed"
        row.completed_at = datetime.now(timezone.utc)
    elif row.progress_percent > 0:
        row.status = "in_progress"

    db.commit()
    db.refresh(row)
    return row

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.session import StudySessionStart, StudySessionRead, StudySessionEnd
from app.services.session_service import start_session, end_session, list_sessions, get_active_session
from app.services.activity_service import record_study
from app.services.streak_service import update_streak

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/start", response_model=StudySessionRead)
def start_study_session(
    data: StudySessionStart,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return start_session(db, current_user.id, data.language_id, data.note)


@router.post("/{session_id}/end", response_model=StudySessionRead)
def end_study_session(
    session_id: int,
    data: StudySessionEnd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = end_session(db, current_user.id, session_id, data.exercises_done)
    minutes = max(1, session.duration_seconds // 60)
    record_study(db, current_user, minutes=minutes, exercises_done=session.exercises_done, xp=minutes * 2)
    update_streak(db, current_user.id)
    return session


@router.get("/active", response_model=StudySessionRead | None)
def active_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_active_session(db, current_user.id)


@router.get("/", response_model=list[StudySessionRead])
def my_sessions(
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_sessions(db, current_user.id, limit)

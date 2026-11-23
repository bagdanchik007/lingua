from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.session import StudySession
from app.utils.exceptions import NotFoundError, BadRequestError


def start_session(db: Session, user_id: int, language_id: int | None = None, note: str | None = None) -> StudySession:
    active = (
        db.query(StudySession)
        .filter(StudySession.user_id == user_id, StudySession.is_active == True)
        .first()
    )
    if active:
        raise BadRequestError("Es läuft bereits eine Session. Bitte zuerst beenden.")

    row = StudySession(user_id=user_id, language_id=language_id, note=note, is_active=True)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def end_session(db: Session, user_id: int, session_id: int, exercises_done: int = 0) -> StudySession:
    row = (
        db.query(StudySession)
        .filter(StudySession.id == session_id, StudySession.user_id == user_id)
        .first()
    )
    if not row:
        raise NotFoundError("Session not found")
    if not row.is_active:
        raise BadRequestError("Session ist bereits beendet")

    now = datetime.now(timezone.utc)
    row.ended_at = now
    row.is_active = False
    row.exercises_done = max(0, exercises_done)
    delta = now - row.started_at
    row.duration_seconds = max(0, int(delta.total_seconds()))
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_sessions(db: Session, user_id: int, limit: int = 20) -> list[StudySession]:
    return (
        db.query(StudySession)
        .filter(StudySession.user_id == user_id)
        .order_by(StudySession.started_at.desc())
        .limit(limit)
        .all()
    )


def get_active_session(db: Session, user_id: int) -> StudySession | None:
    return (
        db.query(StudySession)
        .filter(StudySession.user_id == user_id, StudySession.is_active == True)
        .first()
    )

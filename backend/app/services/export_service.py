"""GDPR-ähnlicher Datenexport für einen User."""
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.progress import ExerciseResult, UserProgress
from app.models.review import UserStreak, ReviewHistory
from app.models.activity import DailyActivity
from app.models.notification import Notification
from app.models.conversation import Conversation, ChatMessage


def export_user_data(db: Session, user: User) -> dict:
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "preferred_language_code": user.preferred_language_code,
            "daily_goal_minutes": user.daily_goal_minutes,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        },
        "exercise_results_count": db.query(ExerciseResult).filter(ExerciseResult.user_id == user.id).count(),
        "progress_count": db.query(UserProgress).filter(UserProgress.user_id == user.id).count(),
        "streak": _streak(db, user.id),
        "daily_activities": _activities(db, user.id),
        "notifications_count": db.query(Notification).filter(Notification.user_id == user.id).count(),
        "conversations": _conversations(db, user.id),
        "review_history_count": db.query(ReviewHistory).filter(ReviewHistory.user_id == user.id).count(),
    }


def _streak(db: Session, user_id: int) -> dict | None:
    s = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
    if not s:
        return None
    return {
        "current_streak": s.current_streak,
        "longest_streak": s.longest_streak,
    }


def _activities(db: Session, user_id: int) -> list[dict]:
    rows = (
        db.query(DailyActivity)
        .filter(DailyActivity.user_id == user_id)
        .order_by(DailyActivity.activity_date.desc())
        .limit(30)
        .all()
    )
    return [
        {
            "date": r.activity_date.isoformat(),
            "minutes": r.minutes_studied,
            "xp": r.xp_earned,
            "goal_reached": r.goal_reached,
        }
        for r in rows
    ]


def _conversations(db: Session, user_id: int) -> list[dict]:
    convs = (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(20)
        .all()
    )
    result = []
    for c in convs:
        msg_count = db.query(ChatMessage).filter(ChatMessage.conversation_id == c.id).count()
        result.append(
            {
                "id": c.id,
                "title": c.title,
                "mode": c.mode,
                "language_code": c.language_code,
                "message_count": msg_count,
            }
        )
    return result

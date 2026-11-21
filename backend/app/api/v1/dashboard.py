from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.progress_service import get_user_stats
from app.services.streak_service import get_streak
from app.services.weakness_service import get_grammar_weaknesses, get_vocabulary_weaknesses
from app.services.activity_service import get_or_create_today, get_week_summary
from app.services.vocabulary_service import get_due_vocabulary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stats = get_user_stats(db, current_user.id)
    streak = get_streak(db, current_user.id)
    today = get_or_create_today(db, current_user.id)
    week = get_week_summary(db, current_user.id)
    due = get_due_vocabulary(db, current_user.id, limit=5)
    grammar_weak = get_grammar_weaknesses(db, current_user.id, limit=3)

    return {
        "user": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "preferred_language_code": current_user.preferred_language_code,
            "daily_goal_minutes": current_user.daily_goal_minutes,
        },
        "stats": stats,
        "streak": streak,
        "today": {
            "minutes_studied": today.minutes_studied,
            "exercises_done": today.exercises_done,
            "xp_earned": today.xp_earned,
            "goal_reached": today.goal_reached,
            "goal_minutes": current_user.daily_goal_minutes or 15,
        },
        "week": week,
        "due_vocabulary_count": len(due),
        "top_grammar_weaknesses": grammar_weak,
    }

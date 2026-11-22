from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.activity import DailyActivity
from app.models.user import User


def xp_leaderboard(db: Session, limit: int = 20) -> list[dict]:
    rows = (
        db.query(
            DailyActivity.user_id,
            func.sum(DailyActivity.xp_earned).label("total_xp"),
            func.sum(DailyActivity.minutes_studied).label("total_minutes"),
        )
        .group_by(DailyActivity.user_id)
        .order_by(func.sum(DailyActivity.xp_earned).desc())
        .limit(limit)
        .all()
    )
    result = []
    for rank, row in enumerate(rows, start=1):
        user = db.query(User).filter(User.id == row.user_id).first()
        result.append(
            {
                "rank": rank,
                "user_id": row.user_id,
                "display_name": (user.full_name or user.email) if user else f"User {row.user_id}",
                "total_xp": int(row.total_xp or 0),
                "total_minutes": int(row.total_minutes or 0),
            }
        )
    return result

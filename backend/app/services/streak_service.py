from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from app.models.review import UserStreak


def update_streak(db: Session, user_id: int) -> UserStreak:
    """Aktualisiert den Lern-Streak des Users."""
    streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
    now = datetime.now(timezone.utc)
    today = now.date()

    if not streak:
        streak = UserStreak(
            user_id=user_id,
            current_streak=1,
            longest_streak=1,
            last_activity_date=now,
        )
        db.add(streak)
        db.commit()
        db.refresh(streak)
        return streak

    if streak.last_activity_date:
        last_date = streak.last_activity_date.date()
        delta = (today - last_date).days

        if delta == 0:
            # Schon heute aktiv gewesen
            pass
        elif delta == 1:
            # Nächster Tag → Streak erhöhen
            streak.current_streak += 1
            if streak.current_streak > streak.longest_streak:
                streak.longest_streak = streak.current_streak
            streak.last_activity_date = now
        else:
            # Streak gebrochen
            streak.current_streak = 1
            streak.last_activity_date = now
    else:
        streak.current_streak = 1
        streak.last_activity_date = now

    db.commit()
    db.refresh(streak)
    return streak


def get_streak(db: Session, user_id: int) -> dict:
    streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
    if not streak:
        return {"current_streak": 0, "longest_streak": 0, "last_activity_date": None}
    return {
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
        "last_activity_date": streak.last_activity_date,
    }

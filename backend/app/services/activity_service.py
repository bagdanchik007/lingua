from datetime import date, datetime, timezone
from sqlalchemy.orm import Session

from app.models.activity import DailyActivity
from app.models.user import User


def get_or_create_today(db: Session, user_id: int) -> DailyActivity:
    today = date.today()
    row = (
        db.query(DailyActivity)
        .filter(DailyActivity.user_id == user_id, DailyActivity.activity_date == today)
        .first()
    )
    if row:
        return row
    row = DailyActivity(user_id=user_id, activity_date=today)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def record_study(
    db: Session,
    user: User,
    minutes: int = 0,
    exercises_done: int = 0,
    exercises_correct: int = 0,
    xp: int = 0,
) -> DailyActivity:
    row = get_or_create_today(db, user.id)
    row.minutes_studied += max(0, minutes)
    row.exercises_done += max(0, exercises_done)
    row.exercises_correct += max(0, exercises_correct)
    row.xp_earned += max(0, xp)
    goal = user.daily_goal_minutes or 15
    row.goal_reached = row.minutes_studied >= goal
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_week_summary(db: Session, user_id: int) -> list[dict]:
    rows = (
        db.query(DailyActivity)
        .filter(DailyActivity.user_id == user_id)
        .order_by(DailyActivity.activity_date.desc())
        .limit(7)
        .all()
    )
    return [
        {
            "date": r.activity_date.isoformat(),
            "minutes_studied": r.minutes_studied,
            "exercises_done": r.exercises_done,
            "xp_earned": r.xp_earned,
            "goal_reached": r.goal_reached,
        }
        for r in reversed(rows)
    ]

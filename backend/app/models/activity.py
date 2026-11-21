from datetime import datetime, timezone, date
from sqlalchemy import Integer, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DailyActivity(Base):
    """Tägliche Lernaktivität pro User (für Goals & Streaks)."""
    __tablename__ = "daily_activities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    activity_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    minutes_studied: Mapped[int] = mapped_column(Integer, default=0)
    exercises_done: Mapped[int] = mapped_column(Integer, default=0)
    exercises_correct: Mapped[int] = mapped_column(Integer, default=0)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0)
    goal_reached: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

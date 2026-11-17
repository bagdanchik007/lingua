from datetime import datetime, timezone
from sqlalchemy import Integer, ForeignKey, DateTime, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ReviewHistory(Base):
    """Speichert jede einzelne Bewertung einer Vokabel"""
    __tablename__ = "review_history"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    vocabulary_id: Mapped[int] = mapped_column(ForeignKey("vocabulary.id"), nullable=False, index=True)
    quality: Mapped[int] = mapped_column(Integer, nullable=False)  # 0-5
    ease_factor_before: Mapped[float] = mapped_column(Float, nullable=True)
    ease_factor_after: Mapped[float] = mapped_column(Float, nullable=True)
    interval_before: Mapped[int] = mapped_column(Integer, nullable=True)
    interval_after: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class UserStreak(Base):
    __tablename__ = "user_streaks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0)
    last_activity_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

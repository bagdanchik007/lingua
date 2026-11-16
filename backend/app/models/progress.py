from sqlalchemy import String, Integer, ForeignKey, DateTime, Float, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from app.core.database import Base


class UserProgress(Base):
    __tablename__ = "user_progress"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    level_id: Mapped[int | None] = mapped_column(ForeignKey("levels.id"), nullable=True)
    grammar_topic_id: Mapped[int | None] = mapped_column(ForeignKey("grammar_topics.id"), nullable=True)
    
    status: Mapped[str] = mapped_column(String(30), default="not_started")  # not_started, in_progress, completed
    progress_percent: Mapped[float] = mapped_column(Float, default=0.0)
    exercises_done: Mapped[int] = mapped_column(Integer, default=0)
    exercises_correct: Mapped[int] = mapped_column(Integer, default=0)
    
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class ExerciseResult(Base):
    __tablename__ = "exercise_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    grammar_topic_id: Mapped[int | None] = mapped_column(ForeignKey("grammar_topics.id"), nullable=True)
    vocabulary_id: Mapped[int | None] = mapped_column(ForeignKey("vocabulary.id"), nullable=True)
    exercise_type: Mapped[str] = mapped_column(String(50), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    user_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    correct_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

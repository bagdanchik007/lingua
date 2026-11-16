from sqlalchemy import String, Text, Integer, ForeignKey, Boolean, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.core.database import Base


class Vocabulary(Base):
    __tablename__ = "vocabulary"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    word: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    translation: Mapped[str] = mapped_column(String(300), nullable=False)
    example_sentence: Mapped[str | None] = mapped_column(Text, nullable=True)
    example_translation: Mapped[str | None] = mapped_column(Text, nullable=True)
    word_type: Mapped[str | None] = mapped_column(String(50), nullable=True)  # noun, verb...
    level_id: Mapped[int | None] = mapped_column(ForeignKey("levels.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    language = relationship("Language", back_populates="vocabulary_items")


class UserVocabulary(Base):
    """Spaced Repetition data per user per word"""
    __tablename__ = "user_vocabulary"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    vocabulary_id: Mapped[int] = mapped_column(ForeignKey("vocabulary.id"), nullable=False)
    ease_factor: Mapped[float] = mapped_column(Float, default=2.5)
    interval_days: Mapped[int] = mapped_column(Integer, default=1)
    repetitions: Mapped[int] = mapped_column(Integer, default=0)
    next_review: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    last_reviewed: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    correct_count: Mapped[int] = mapped_column(Integer, default=0)
    incorrect_count: Mapped[int] = mapped_column(Integer, default=0)

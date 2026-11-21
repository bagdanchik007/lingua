from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, ForeignKey, Boolean, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Exercise(Base):
    """Übungsvorlage (Multiple Choice, Lücke, Satzbau, ...)."""
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False, index=True)
    level_id: Mapped[int | None] = mapped_column(ForeignKey("levels.id"), nullable=True)
    grammar_topic_id: Mapped[int | None] = mapped_column(ForeignKey("grammar_topics.id"), nullable=True)
    vocabulary_id: Mapped[int | None] = mapped_column(ForeignKey("vocabulary.id"), nullable=True)

    exercise_type: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    correct_answer: Mapped[str] = mapped_column(Text, nullable=False)
    alternatives: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

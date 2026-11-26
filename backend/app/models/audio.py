from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SpeakingAttempt(Base):
    """Gespeicherte Sprechversuche (SprechenOrt)."""
    __tablename__ = "speaking_attempts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    language_code: Mapped[str] = mapped_column(String(10), default="de")
    reference_text: Mapped[str] = mapped_column(Text, nullable=False)
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

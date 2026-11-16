from sqlalchemy import String, Text, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class GrammarTopic(Base):
    __tablename__ = "grammar_topics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    examples: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    language = relationship("Language", back_populates="grammar_topics")
    level = relationship("Level", back_populates="grammar_topics")

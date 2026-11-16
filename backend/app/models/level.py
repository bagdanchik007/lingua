from sqlalchemy import String, Text, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Level(Base):
    __tablename__ = "levels"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)  # e.g. "A1.1", "B2.2"
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    cefr_level: Mapped[str] = mapped_column(String(5), nullable=False)  # A1, A2, B1...
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    language = relationship("Language", back_populates="levels")
    grammar_topics = relationship("GrammarTopic", back_populates="level")

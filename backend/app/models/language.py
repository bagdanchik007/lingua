from sqlalchemy import String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, index=True)  # e.g. "de", "en"
    name: Mapped[str] = mapped_column(String(100), nullable=False)          # e.g. "Deutsch"
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)       # e.g. "German"
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    levels = relationship("Level", back_populates="language")
    grammar_topics = relationship("GrammarTopic", back_populates="language")
    vocabulary_items = relationship("Vocabulary", back_populates="language")

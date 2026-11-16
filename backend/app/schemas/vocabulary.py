from datetime import datetime
from pydantic import BaseModel


class VocabularyBase(BaseModel):
    word: str
    translation: str
    example_sentence: str | None = None
    example_translation: str | None = None
    word_type: str | None = None
    is_active: bool = True


class VocabularyCreate(VocabularyBase):
    language_id: int
    level_id: int | None = None


class VocabularyRead(VocabularyBase):
    id: int
    language_id: int
    level_id: int | None = None

    model_config = {"from_attributes": True}


class UserVocabularyRead(BaseModel):
    id: int
    vocabulary_id: int
    ease_factor: float
    interval_days: int
    repetitions: int
    next_review: datetime
    correct_count: int
    incorrect_count: int
    vocabulary: VocabularyRead | None = None

    model_config = {"from_attributes": True}


class ReviewResult(BaseModel):
    vocabulary_id: int
    quality: int  # 0-5 (SM-2 style)

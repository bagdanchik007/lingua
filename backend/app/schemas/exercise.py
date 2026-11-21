from pydantic import BaseModel, Field


class ExerciseBase(BaseModel):
    exercise_type: str
    prompt: str
    correct_answer: str
    alternatives: dict | None = None
    explanation: str | None = None
    difficulty: int = Field(default=1, ge=1, le=5)


class ExerciseCreate(ExerciseBase):
    language_id: int
    level_id: int | None = None
    grammar_topic_id: int | None = None
    vocabulary_id: int | None = None


class ExerciseRead(ExerciseBase):
    id: int
    language_id: int
    level_id: int | None = None
    grammar_topic_id: int | None = None
    vocabulary_id: int | None = None
    is_active: bool = True

    model_config = {"from_attributes": True}


class ExerciseAnswer(BaseModel):
    exercise_id: int
    user_answer: str


class ExerciseCheckResult(BaseModel):
    exercise_id: int
    is_correct: bool
    correct_answer: str
    explanation: str | None = None
    xp_gained: int = 0

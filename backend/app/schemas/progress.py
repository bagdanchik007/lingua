from datetime import datetime
from pydantic import BaseModel


class UserProgressBase(BaseModel):
    language_id: int
    level_id: int | None = None
    grammar_topic_id: int | None = None
    status: str = "not_started"
    progress_percent: float = 0.0


class UserProgressRead(UserProgressBase):
    id: int
    user_id: int
    exercises_done: int
    exercises_correct: int
    started_at: datetime | None = None
    completed_at: datetime | None = None
    updated_at: datetime

    model_config = {"from_attributes": True}


class ExerciseSubmit(BaseModel):
    grammar_topic_id: int | None = None
    vocabulary_id: int | None = None
    exercise_type: str
    is_correct: bool
    user_answer: str | None = None
    correct_answer: str | None = None


class ExerciseResultRead(BaseModel):
    id: int
    exercise_type: str
    is_correct: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserStats(BaseModel):
    total_exercises: int
    correct_exercises: int
    accuracy: float
    vocabulary_learned: int
    grammar_topics_completed: int
    current_streak: int = 0

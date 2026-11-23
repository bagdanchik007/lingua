from datetime import datetime
from pydantic import BaseModel


class StudySessionStart(BaseModel):
    language_id: int | None = None
    note: str | None = None


class StudySessionRead(BaseModel):
    id: int
    user_id: int
    language_id: int | None
    started_at: datetime
    ended_at: datetime | None
    duration_seconds: int
    exercises_done: int
    is_active: bool
    note: str | None = None

    model_config = {"from_attributes": True}


class StudySessionEnd(BaseModel):
    exercises_done: int = 0

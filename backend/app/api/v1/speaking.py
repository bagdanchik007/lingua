from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.speaking_service import evaluate_speaking, list_attempts
from app.utils.rate_limit import ai_rate_limiter

router = APIRouter(prefix="/speaking", tags=["speaking"])


class SpeakingEvaluateIn(BaseModel):
    reference_text: str = Field(..., min_length=1, max_length=1000)
    transcript: str | None = Field(default=None, max_length=2000)
    language_code: str = "de"


class SpeakingAttemptRead(BaseModel):
    id: int
    reference_text: str
    transcript: str | None
    score: float
    feedback: str | None
    language_code: str

    model_config = {"from_attributes": True}


@router.post("/evaluate", response_model=SpeakingAttemptRead)
def evaluate(
    data: SpeakingEvaluateIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ai_rate_limiter.check_or_raise(f"ai:speaking:{current_user.id}")
    return evaluate_speaking(
        db,
        current_user.id,
        data.reference_text,
        data.transcript,
        data.language_code,
    )


@router.get("/attempts", response_model=list[SpeakingAttemptRead])
def my_attempts(
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_attempts(db, current_user.id, limit)

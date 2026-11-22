from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.core.logging import logger

router = APIRouter(prefix="/feedback", tags=["feedback"])


class FeedbackIn(BaseModel):
    message: str = Field(..., min_length=5, max_length=2000)
    category: str = "general"
    page: str | None = None


@router.post("/")
def submit_feedback(
    data: FeedbackIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Foundation: loggen; später eigene Tabelle / Ticket-System
    logger.info(
        "feedback user_id=%s category=%s page=%s message=%s",
        current_user.id,
        data.category,
        data.page,
        data.message[:200],
    )
    return {"status": "received", "message": "Danke für dein Feedback!"}

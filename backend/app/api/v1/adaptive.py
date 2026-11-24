from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.adaptive_service import recommend_next_steps

router = APIRouter(prefix="/adaptive", tags=["adaptive"])


@router.get("/next")
def next_steps(
    language_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return recommend_next_steps(db, current_user.id, language_id)

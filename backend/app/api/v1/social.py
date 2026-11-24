from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.social_service import (
    create_partner_request,
    list_open_requests,
    match_request,
)

router = APIRouter(prefix="/social", tags=["social"])


class PartnerRequestCreate(BaseModel):
    language_code: str = Field(..., min_length=2, max_length=10)
    level_cefr: str | None = None
    message: str | None = Field(default=None, max_length=500)


class PartnerRequestRead(BaseModel):
    id: int
    user_id: int
    language_code: str
    level_cefr: str | None
    message: str | None
    status: str

    model_config = {"from_attributes": True}


@router.post("/partner-requests", response_model=PartnerRequestRead)
def create_request(
    data: PartnerRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_partner_request(
        db, current_user.id, data.language_code, data.level_cefr, data.message
    )


@router.get("/partner-requests", response_model=list[PartnerRequestRead])
def open_requests(
    language_code: str | None = None,
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_open_requests(db, language_code, limit)


@router.post("/partner-requests/{request_id}/match", response_model=PartnerRequestRead)
def match(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return match_request(db, request_id, current_user.id)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, get_current_active_superuser
from app.models.user import User
from app.schemas.report import ContentReportCreate, ContentReportRead
from app.services.report_service import create_report, list_open_reports, resolve_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/", response_model=ContentReportRead)
def submit_report(
    data: ContentReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_report(db, current_user.id, data)


@router.get("/open", response_model=list[ContentReportRead])
def open_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    return list_open_reports(db)


@router.post("/{report_id}/resolve", response_model=ContentReportRead)
def resolve(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    row = resolve_report(db, report_id)
    if not row:
        raise HTTPException(status_code=404, detail="Report not found")
    return row

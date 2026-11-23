from sqlalchemy.orm import Session

from app.models.report import ContentReport
from app.schemas.report import ContentReportCreate


def create_report(db: Session, user_id: int, data: ContentReportCreate) -> ContentReport:
    row = ContentReport(user_id=user_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_open_reports(db: Session, limit: int = 50) -> list[ContentReport]:
    return (
        db.query(ContentReport)
        .filter(ContentReport.is_resolved == False)
        .order_by(ContentReport.created_at.desc())
        .limit(limit)
        .all()
    )


def resolve_report(db: Session, report_id: int) -> ContentReport | None:
    row = db.query(ContentReport).filter(ContentReport.id == report_id).first()
    if not row:
        return None
    row.is_resolved = True
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

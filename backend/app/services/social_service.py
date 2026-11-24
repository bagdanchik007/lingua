from sqlalchemy.orm import Session

from app.models.social import PracticePartnerRequest
from app.utils.exceptions import NotFoundError, BadRequestError


def create_partner_request(
    db: Session,
    user_id: int,
    language_code: str,
    level_cefr: str | None = None,
    message: str | None = None,
) -> PracticePartnerRequest:
    open_req = (
        db.query(PracticePartnerRequest)
        .filter(
            PracticePartnerRequest.user_id == user_id,
            PracticePartnerRequest.status == "open",
            PracticePartnerRequest.is_active == True,
        )
        .first()
    )
    if open_req:
        raise BadRequestError("Du hast bereits eine offene Anfrage.")

    row = PracticePartnerRequest(
        user_id=user_id,
        language_code=language_code,
        level_cefr=level_cefr,
        message=message,
        status="open",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_open_requests(db: Session, language_code: str | None = None, limit: int = 20):
    q = db.query(PracticePartnerRequest).filter(
        PracticePartnerRequest.status == "open",
        PracticePartnerRequest.is_active == True,
    )
    if language_code:
        q = q.filter(PracticePartnerRequest.language_code == language_code)
    return q.order_by(PracticePartnerRequest.created_at.desc()).limit(limit).all()


def match_request(db: Session, request_id: int, matcher_user_id: int) -> PracticePartnerRequest:
    row = db.query(PracticePartnerRequest).filter(PracticePartnerRequest.id == request_id).first()
    if not row or row.status != "open":
        raise NotFoundError("Request not available")
    if row.user_id == matcher_user_id:
        raise BadRequestError("Du kannst dich nicht selbst matchen.")
    row.status = "matched"
    row.matched_user_id = matcher_user_id
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

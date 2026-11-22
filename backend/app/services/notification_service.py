from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate


def create_notification(db: Session, user_id: int, data: NotificationCreate) -> Notification:
    row = Notification(user_id=user_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_notifications(db: Session, user_id: int, unread_only: bool = False, limit: int = 50):
    q = db.query(Notification).filter(Notification.user_id == user_id)
    if unread_only:
        q = q.filter(Notification.is_read == False)
    return q.order_by(Notification.created_at.desc()).limit(limit).all()


def mark_read(db: Session, user_id: int, notification_id: int) -> Notification | None:
    row = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == user_id)
        .first()
    )
    if not row:
        return None
    row.is_read = True
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def mark_all_read(db: Session, user_id: int) -> int:
    rows = (
        db.query(Notification)
        .filter(Notification.user_id == user_id, Notification.is_read == False)
        .all()
    )
    for r in rows:
        r.is_read = True
        db.add(r)
    db.commit()
    return len(rows)


def notify_achievement(db: Session, user_id: int, title: str, body: str) -> Notification:
    return create_notification(
        db,
        user_id,
        NotificationCreate(title=title, body=body, category="achievement"),
    )

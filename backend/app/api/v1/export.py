from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.export_service import export_user_data
from app.services.audit_service import log_action

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/me")
def export_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = export_user_data(db, current_user)
    log_action(db, "export.user_data", user_id=current_user.id, resource_type="user", resource_id=current_user.id)
    return data

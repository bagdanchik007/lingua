from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_active_superuser
from app.models.user import User
from app.services.metrics_service import platform_metrics

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/platform")
def get_platform_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    return platform_metrics(db)

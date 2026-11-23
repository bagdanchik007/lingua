from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.favorite import FavoriteCreate, FavoriteRead
from app.services.favorite_service import add_favorite, remove_favorite, list_favorites

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("/", response_model=list[FavoriteRead])
def get_favorites(
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_favorites(db, current_user.id, limit)


@router.post("/", response_model=FavoriteRead)
def create_favorite(
    data: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return add_favorite(db, current_user.id, data.vocabulary_id)


@router.delete("/{vocabulary_id}")
def delete_favorite(
    vocabulary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    remove_favorite(db, current_user.id, vocabulary_id)
    return {"status": "removed"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.language import Language
from app.models.level import Level
from app.schemas.language import LanguageRead, LanguageCreate
from app.schemas.level import LevelRead, LevelCreate
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/languages", tags=["languages"])


@router.get("/", response_model=list[LanguageRead])
def list_languages(db: Session = Depends(get_db)):
    return db.query(Language).filter(Language.is_active == True).all()


@router.post("/", response_model=LanguageRead)
def create_language(
    data: LanguageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lang = Language(**data.model_dump())
    db.add(lang)
    db.commit()
    db.refresh(lang)
    return lang


@router.get("/{language_id}/levels", response_model=list[LevelRead])
def list_levels(language_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Level)
        .filter(Level.language_id == language_id, Level.is_active == True)
        .order_by(Level.order)
        .all()
    )


@router.post("/levels", response_model=LevelRead)
def create_level(
    data: LevelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    level = Level(**data.model_dump())
    db.add(level)
    db.commit()
    db.refresh(level)
    return level

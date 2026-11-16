from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.vocabulary import (
    VocabularyRead,
    VocabularyCreate,
    UserVocabularyRead,
    ReviewResult,
)
from app.services.vocabulary_service import (
    create_vocabulary,
    get_vocabulary_by_language,
    get_due_vocabulary,
    process_review,
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/vocabulary", tags=["vocabulary"])


@router.get("/", response_model=list[VocabularyRead])
def list_vocabulary(language_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return get_vocabulary_by_language(db, language_id, skip, limit)


@router.post("/", response_model=VocabularyRead)
def add_vocabulary(
    data: VocabularyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_vocabulary(db, data)


@router.get("/due", response_model=list[UserVocabularyRead])
def get_due_words(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_due_vocabulary(db, current_user.id, limit)


@router.post("/review", response_model=UserVocabularyRead)
def review_word(
    review: ReviewResult,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return process_review(db, current_user.id, review)

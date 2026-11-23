from sqlalchemy.orm import Session

from app.models.favorite import FavoriteVocabulary
from app.models.vocabulary import Vocabulary
from app.utils.exceptions import NotFoundError, ConflictError


def add_favorite(db: Session, user_id: int, vocabulary_id: int) -> FavoriteVocabulary:
    vocab = db.query(Vocabulary).filter(Vocabulary.id == vocabulary_id, Vocabulary.is_active == True).first()
    if not vocab:
        raise NotFoundError("Vocabulary not found")

    exists = (
        db.query(FavoriteVocabulary)
        .filter(
            FavoriteVocabulary.user_id == user_id,
            FavoriteVocabulary.vocabulary_id == vocabulary_id,
        )
        .first()
    )
    if exists:
        raise ConflictError("Already in favorites")

    row = FavoriteVocabulary(user_id=user_id, vocabulary_id=vocabulary_id)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def remove_favorite(db: Session, user_id: int, vocabulary_id: int) -> None:
    row = (
        db.query(FavoriteVocabulary)
        .filter(
            FavoriteVocabulary.user_id == user_id,
            FavoriteVocabulary.vocabulary_id == vocabulary_id,
        )
        .first()
    )
    if not row:
        raise NotFoundError("Favorite not found")
    db.delete(row)
    db.commit()


def list_favorites(db: Session, user_id: int, limit: int = 50) -> list[FavoriteVocabulary]:
    return (
        db.query(FavoriteVocabulary)
        .filter(FavoriteVocabulary.user_id == user_id)
        .order_by(FavoriteVocabulary.created_at.desc())
        .limit(limit)
        .all()
    )

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.models.vocabulary import Vocabulary, UserVocabulary
from app.schemas.vocabulary import VocabularyCreate, ReviewResult


def create_vocabulary(db: Session, item: VocabularyCreate) -> Vocabulary:
    db_item = Vocabulary(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_vocabulary_by_language(db: Session, language_id: int, skip: int = 0, limit: int = 50):
    return (
        db.query(Vocabulary)
        .filter(Vocabulary.language_id == language_id, Vocabulary.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_due_vocabulary(db: Session, user_id: int, limit: int = 20):
    now = datetime.now(timezone.utc)
    return (
        db.query(UserVocabulary)
        .filter(
            UserVocabulary.user_id == user_id,
            UserVocabulary.next_review <= now,
        )
        .limit(limit)
        .all()
    )


def process_review(db: Session, user_id: int, review: ReviewResult) -> UserVocabulary:
    """Einfacher SM-2 basierter Spaced Repetition Algorithmus"""
    uv = (
        db.query(UserVocabulary)
        .filter(
            UserVocabulary.user_id == user_id,
            UserVocabulary.vocabulary_id == review.vocabulary_id,
        )
        .first()
    )

    if not uv:
        uv = UserVocabulary(
            user_id=user_id,
            vocabulary_id=review.vocabulary_id,
        )
        db.add(uv)

    quality = max(0, min(5, review.quality))

    if quality >= 3:
        if uv.repetitions == 0:
            uv.interval_days = 1
        elif uv.repetitions == 1:
            uv.interval_days = 3
        else:
            uv.interval_days = int(uv.interval_days * uv.ease_factor)
        uv.repetitions += 1
        uv.correct_count += 1
    else:
        uv.repetitions = 0
        uv.interval_days = 1
        uv.incorrect_count += 1

    # Ease Factor anpassen
    uv.ease_factor = max(1.3, uv.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
    uv.last_reviewed = datetime.now(timezone.utc)
    uv.next_review = uv.last_reviewed + timedelta(days=uv.interval_days)

    db.commit()
    db.refresh(uv)
    return uv

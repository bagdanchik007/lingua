from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.models.vocabulary import Vocabulary, UserVocabulary
from app.models.review import ReviewHistory
from app.schemas.vocabulary import VocabularyCreate, ReviewResult


def create_vocabulary(db: Session, item: VocabularyCreate) -> Vocabulary:
    db_item = Vocabulary(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_vocabulary_by_language(
    db: Session,
    language_id: int,
    skip: int = 0,
    limit: int = 50,
    search: str | None = None,
):
    query = db.query(Vocabulary).filter(
        Vocabulary.language_id == language_id,
        Vocabulary.is_active == True,
    )
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Vocabulary.word.ilike(pattern),
                Vocabulary.translation.ilike(pattern),
            )
        )
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def get_due_vocabulary(db: Session, user_id: int, limit: int = 20):
    now = datetime.now(timezone.utc)
    return (
        db.query(UserVocabulary)
        .filter(
            UserVocabulary.user_id == user_id,
            UserVocabulary.next_review <= now,
        )
        .order_by(UserVocabulary.next_review.asc())
        .limit(limit)
        .all()
    )


def process_review(db: Session, user_id: int, review: ReviewResult) -> UserVocabulary:
    """SM-2 basierter Spaced Repetition Algorithmus + ReviewHistory"""
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
        db.flush()

    quality = max(0, min(5, review.quality))
    ease_before = uv.ease_factor
    interval_before = uv.interval_days

    if quality >= 3:
        if uv.repetitions == 0:
            uv.interval_days = 1
        elif uv.repetitions == 1:
            uv.interval_days = 3
        else:
            uv.interval_days = max(1, int(uv.interval_days * uv.ease_factor))
        uv.repetitions += 1
        uv.correct_count += 1
    else:
        uv.repetitions = 0
        uv.interval_days = 1
        uv.incorrect_count += 1

    uv.ease_factor = max(
        1.3,
        uv.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)),
    )
    uv.last_reviewed = datetime.now(timezone.utc)
    uv.next_review = uv.last_reviewed + timedelta(days=uv.interval_days)

    # Review-Historie speichern
    history = ReviewHistory(
        user_id=user_id,
        vocabulary_id=review.vocabulary_id,
        quality=quality,
        ease_factor_before=ease_before,
        ease_factor_after=uv.ease_factor,
        interval_before=interval_before,
        interval_after=uv.interval_days,
    )
    db.add(history)

    db.commit()
    db.refresh(uv)
    return uv


def search_vocabulary(db: Session, q: str, language_id: int | None = None, limit: int = 20):
    pattern = f"%{q}%"
    query = db.query(Vocabulary).filter(
        Vocabulary.is_active == True,
        or_(
            Vocabulary.word.ilike(pattern),
            Vocabulary.translation.ilike(pattern),
        ),
    )
    if language_id:
        query = query.filter(Vocabulary.language_id == language_id)
    return query.limit(limit).all()

"""Einfacher Content-Import (JSON-Listen) für Vokabeln."""
from sqlalchemy.orm import Session

from app.models.vocabulary import Vocabulary


def import_vocabulary_items(db: Session, language_id: int, items: list[dict]) -> dict:
    created = 0
    skipped = 0
    for item in items:
        word = (item.get("word") or "").strip()
        translation = (item.get("translation") or "").strip()
        if not word or not translation:
            skipped += 1
            continue
        exists = (
            db.query(Vocabulary)
            .filter(
                Vocabulary.language_id == language_id,
                Vocabulary.word == word,
                Vocabulary.translation == translation,
            )
            .first()
        )
        if exists:
            skipped += 1
            continue
        db.add(
            Vocabulary(
                language_id=language_id,
                word=word,
                translation=translation,
                example_sentence=item.get("example_sentence"),
                example_translation=item.get("example_translation"),
                word_type=item.get("word_type"),
                level_id=item.get("level_id"),
                is_active=True,
            )
        )
        created += 1
    db.commit()
    return {"created": created, "skipped": skipped}

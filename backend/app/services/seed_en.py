"""Zusätzlicher EN-Content für Seed."""
from sqlalchemy.orm import Session

from app.models.language import Language
from app.models.vocabulary import Vocabulary
from app.models.grammar import GrammarTopic
from app.models.level import Level


EN_VOCAB = [
    ("hello", "hallo", "greeting"),
    ("goodbye", "tschüss", "greeting"),
    ("please", "bitte", "polite"),
    ("thank you", "danke", "polite"),
    ("yes", "ja", "basic"),
    ("no", "nein", "basic"),
    ("water", "Wasser", "noun"),
    ("bread", "Brot", "noun"),
    ("friend", "Freund", "noun"),
    ("learn", "lernen", "verb"),
]


def seed_english_basics(db: Session) -> dict:
    en = db.query(Language).filter(Language.code == "en").first()
    de = db.query(Language).filter(Language.code == "de").first()
    if not en:
        return {"vocabulary": 0, "grammar": 0}

    created_v = 0
    for word, translation, wtype in EN_VOCAB:
        exists = (
            db.query(Vocabulary)
            .filter(Vocabulary.language_id == en.id, Vocabulary.word == word)
            .first()
        )
        if exists:
            continue
        db.add(
            Vocabulary(
                language_id=en.id,
                word=word,
                translation=translation,
                word_type=wtype,
                is_active=True,
            )
        )
        created_v += 1

    created_g = 0
    if de:
        level = db.query(Level).filter(Level.language_id == de.id, Level.code == "A1.1").first()
        if level:
            slug = "to-be-present"
            exists = db.query(GrammarTopic).filter(GrammarTopic.slug == slug).first()
            if not exists:
                db.add(
                    GrammarTopic(
                        language_id=en.id,
                        level_id=level.id,
                        title="Verb to be (Present)",
                        slug=slug,
                        explanation=(
                            "I am, you are, he/she/it is, we are, you are, they are.\n"
                            "Negation: I am not, you are not / aren't, ..."
                        ),
                        examples="I am a student. She is here. They are friends.",
                        order=10,
                        is_active=True,
                    )
                )
                created_g = 1

    db.commit()
    return {"vocabulary": created_v, "grammar": created_g}

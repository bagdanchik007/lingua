from sqlalchemy.orm import Session

from app.models.language import Language
from app.models.level import Level
from app.models.grammar import GrammarTopic


def seed_languages_and_levels(db: Session) -> dict:
    """Erstellt die Basis-Sprachen und CEFR-Levels falls sie noch nicht existieren."""
    created = {"languages": 0, "levels": 0}

    languages_data = [
        {"code": "de", "name": "Deutsch", "name_en": "German"},
        {"code": "en", "name": "Englisch", "name_en": "English"},
        {"code": "fr", "name": "Französisch", "name_en": "French"},
        {"code": "it", "name": "Italienisch", "name_en": "Italian"},
        {"code": "es", "name": "Spanisch", "name_en": "Spanish"},
        {"code": "ru", "name": "Russisch", "name_en": "Russian"},
    ]

    lang_map = {}
    for data in languages_data:
        existing = db.query(Language).filter(Language.code == data["code"]).first()
        if not existing:
            lang = Language(**data, is_active=True)
            db.add(lang)
            db.flush()
            created["languages"] += 1
            lang_map[data["code"]] = lang
        else:
            lang_map[data["code"]] = existing

    # CEFR Levels für Deutsch als Lernsprache (Beispiel)
    levels_template = [
        ("A1.1", "A1 Einstieg 1", "Artikel, Präsens, einfache Satzstellung", "A1", 1),
        ("A1.2", "A1 Einstieg 2", "Akkusativ/Dativ, Modalverben, trennbare Verben", "A1", 2),
        ("A2.1", "A2 Grundlage 1", "Perfekt, Komparativ, Nebensätze (weil, dass)", "A2", 3),
        ("A2.2", "A2 Grundlage 2", "Präteritum, Präpositionen, indirekte Rede Ansatz", "A2", 4),
        ("B1.1", "B1 Selbstständig 1", "Konjunktiv II, Passiv, Relativsätze", "B1", 5),
        ("B1.2", "B1 Selbstständig 2", "Nominalisierung, erweiterte Nebensätze", "B1", 6),
        ("B2.1", "B2 Fortgeschritten 1", "Konjunktiv I, komplexe Satzgefüge", "B2", 7),
        ("B2.2", "B2 Fortgeschritten 2", "Stilistik, Register, Nuancen", "B2", 8),
    ]

    de = lang_map.get("de")
    if de:
        for code, name, desc, cefr, order in levels_template:
            exists = db.query(Level).filter(Level.language_id == de.id, Level.code == code).first()
            if not exists:
                level = Level(
                    language_id=de.id,
                    code=code,
                    name=name,
                    description=desc,
                    cefr_level=cefr,
                    order=order,
                    is_active=True,
                )
                db.add(level)
                created["levels"] += 1

    db.commit()
    return created


def seed_grammar_topics(db: Session) -> int:
    """Legt einige echte Grammatik-Themen für Deutsch A1 an."""
    de = db.query(Language).filter(Language.code == "de").first()
    if not de:
        return 0

    a11 = db.query(Level).filter(Level.language_id == de.id, Level.code == "A1.1").first()
    a12 = db.query(Level).filter(Level.language_id == de.id, Level.code == "A1.2").first()
    if not a11:
        return 0

    topics = [
        {
            "level": a11,
            "title": "Bestimmte und unbestimmte Artikel",
            "slug": "artikel-nominativ",
            "explanation": (
                "Im Deutschen gibt es bestimmte Artikel (der, die, das) und unbestimmte Artikel (ein, eine).\n\n"
                "Bestimmter Artikel (Nominativ):\n"
                "- Maskulin: der Mann\n"
                "- Feminin: die Frau\n"
                "- Neutral: das Kind\n"
                "- Plural: die Männer / die Frauen / die Kinder\n\n"
                "Unbestimmter Artikel:\n"
                "- Maskulin: ein Mann\n"
                "- Feminin: eine Frau\n"
                "- Neutral: ein Kind\n"
                "- Plural: (kein unbestimmter Artikel)"
            ),
            "examples": "Der Mann liest. Eine Frau spricht. Das Kind spielt.",
            "order": 1,
        },
        {
            "level": a11,
            "title": "Präsens – regelmäßige Verben",
            "slug": "praesens-regelmaessig",
            "explanation": (
                "Regelmäßige Verben bilden das Präsens so:\n"
                "ich lerne, du lernst, er/sie/es lernt,\n"
                "wir lernen, ihr lernt, sie/Sie lernen.\n\n"
                "Die Endungen sind: -e, -st, -t, -en, -t, -en."
            ),
            "examples": "Ich lerne Deutsch. Du lernst Englisch. Wir lernen zusammen.",
            "order": 2,
        },
        {
            "level": a12,
            "title": "Akkusativ",
            "slug": "akkusativ",
            "explanation": (
                "Der Akkusativ ist der 4. Fall. Er antwortet auf die Frage „Wen?“ oder „Was?“.\n\n"
                "Artikel im Akkusativ:\n"
                "- Maskulin: den / einen\n"
                "- Feminin: die / eine\n"
                "- Neutral: das / ein\n"
                "- Plural: die\n\n"
                "Viele Verben brauchen den Akkusativ: sehen, haben, kaufen, lesen, brauchen..."
            ),
            "examples": "Ich sehe den Mann. Sie hat eine Tasche. Wir kaufen das Buch.",
            "order": 1,
        },
        {
            "level": a12,
            "title": "Modalverben",
            "slug": "modalverben",
            "explanation": (
                "Die wichtigsten Modalverben: können, müssen, wollen, dürfen, sollen, mögen.\n\n"
                "Sie stehen in der Regel in Position 2, das Vollverb steht im Infinitiv am Ende.\n"
                "Beispiel: Ich kann Deutsch sprechen."
            ),
            "examples": "Ich kann schwimmen. Du musst lernen. Wir wollen reisen.",
            "order": 2,
        },
    ]

    created = 0
    for t in topics:
        exists = db.query(GrammarTopic).filter(GrammarTopic.slug == t["slug"]).first()
        if not exists and t["level"]:
            topic = GrammarTopic(
                language_id=de.id,
                level_id=t["level"].id,
                title=t["title"],
                slug=t["slug"],
                explanation=t["explanation"],
                examples=t["examples"],
                order=t["order"],
                is_active=True,
            )
            db.add(topic)
            created += 1

    db.commit()
    return created


def seed_sample_exercises(db: Session) -> int:
    """Legt Beispiel-Übungen an, falls Grammatik-Themen existieren."""
    from app.models.exercise import Exercise
    from app.models.grammar import GrammarTopic

    topic = db.query(GrammarTopic).filter(GrammarTopic.slug == "artikel-nominativ").first()
    if not topic:
        return 0
    existing = db.query(Exercise).filter(Exercise.grammar_topic_id == topic.id).count()
    if existing > 0:
        return 0

    samples = [
        {
            "exercise_type": "multiple_choice",
            "prompt": "Welcher Artikel passt? ___ Mann liest.",
            "correct_answer": "Der",
            "alternatives": {"options": ["Der", "Die", "Das", "Den"]},
            "explanation": "Mann ist maskulin → bestimmter Artikel im Nominativ: der.",
            "difficulty": 1,
        },
        {
            "exercise_type": "fill_blank",
            "prompt": "___ Frau spricht Deutsch. (bestimmt, Nominativ)",
            "correct_answer": "Die",
            "alternatives": None,
            "explanation": "Frau ist feminin → die.",
            "difficulty": 1,
        },
    ]
    created = 0
    for s in samples:
        ex = Exercise(
            language_id=topic.language_id,
            level_id=topic.level_id,
            grammar_topic_id=topic.id,
            **s,
        )
        db.add(ex)
        created += 1
    db.commit()
    return created

from sqlalchemy.orm import Session

from app.services.weakness_service import get_grammar_weaknesses, get_vocabulary_weaknesses
from app.services.progress_service import get_user_stats
from app.models.grammar import GrammarTopic
from app.models.level import Level


def recommend_next_steps(db: Session, user_id: int, language_id: int | None = None) -> dict:
    """Einfache adaptive Empfehlungen aus Schwächen + Stats."""
    stats = get_user_stats(db, user_id)
    grammar_weak = get_grammar_weaknesses(db, user_id, limit=5)
    vocab_weak = get_vocabulary_weaknesses(db, user_id, limit=5)

    suggested_grammar = []
    for w in grammar_weak:
        topic = db.query(GrammarTopic).filter(GrammarTopic.id == w["grammar_topic_id"]).first()
        if topic:
            suggested_grammar.append(
                {
                    "id": topic.id,
                    "title": topic.title,
                    "slug": topic.slug,
                    "reason": f"Genauigkeit nur {w['accuracy']}%",
                }
            )

    focus = "grammar" if grammar_weak else "vocabulary"
    if stats.accuracy >= 85 and not grammar_weak:
        focus = "challenge"

    return {
        "focus": focus,
        "accuracy": stats.accuracy,
        "suggested_grammar": suggested_grammar,
        "suggested_vocabulary_ids": [v["vocabulary_id"] for v in vocab_weak],
        "message": _message_for_focus(focus, stats.accuracy),
    }


def _message_for_focus(focus: str, accuracy: float) -> str:
    if focus == "grammar":
        return "Konzentriere dich auf die markierten Grammatik-Themen."
    if focus == "vocabulary":
        return "Wiederhole die schwachen Vokabeln mit SRS."
    return f"Starke Quote ({accuracy}%). Zeit für schwierigere Übungen."

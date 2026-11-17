from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models.progress import ExerciseResult
from app.models.grammar import GrammarTopic
from app.models.vocabulary import UserVocabulary


def get_grammar_weaknesses(db: Session, user_id: int, limit: int = 5) -> list[dict]:
    """Findet Grammatik-Themen mit der schlechtesten Erfolgsquote."""
    results = (
        db.query(
            ExerciseResult.grammar_topic_id,
            func.count(ExerciseResult.id).label("total"),
            func.sum(func.cast(ExerciseResult.is_correct, type_=db.bind.dialect.type_descriptor(type(1)))).label("correct"),
        )
        .filter(
            ExerciseResult.user_id == user_id,
            ExerciseResult.grammar_topic_id.isnot(None),
        )
        .group_by(ExerciseResult.grammar_topic_id)
        .all()
    )

    weaknesses = []
    for row in results:
        total = row.total or 0
        correct = row.correct or 0
        if total < 3:
            continue
        accuracy = (correct / total) * 100
        if accuracy < 75:
            topic = db.query(GrammarTopic).filter(GrammarTopic.id == row.grammar_topic_id).first()
            weaknesses.append({
                "grammar_topic_id": row.grammar_topic_id,
                "title": topic.title if topic else "Unbekannt",
                "total_attempts": total,
                "correct": correct,
                "accuracy": round(accuracy, 1),
            })

    weaknesses.sort(key=lambda x: x["accuracy"])
    return weaknesses[:limit]


def get_vocabulary_weaknesses(db: Session, user_id: int, limit: int = 10) -> list[dict]:
    """Vokabeln mit vielen Fehlern oder niedrigem Ease-Factor."""
    items = (
        db.query(UserVocabulary)
        .filter(UserVocabulary.user_id == user_id)
        .order_by(UserVocabulary.incorrect_count.desc(), UserVocabulary.ease_factor.asc())
        .limit(limit)
        .all()
    )

    result = []
    for uv in items:
        if uv.incorrect_count == 0 and uv.ease_factor >= 2.3:
            continue
        result.append({
            "vocabulary_id": uv.vocabulary_id,
            "incorrect_count": uv.incorrect_count,
            "correct_count": uv.correct_count,
            "ease_factor": round(uv.ease_factor, 2),
            "repetitions": uv.repetitions,
        })
    return result

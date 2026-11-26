from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.progress import ExerciseResult
from app.models.vocabulary import Vocabulary
from app.models.grammar import GrammarTopic
from app.models.conversation import Conversation


def platform_metrics(db: Session) -> dict:
    return {
        "users_total": db.query(func.count(User.id)).scalar() or 0,
        "users_active": db.query(func.count(User.id)).filter(User.is_active == True).scalar() or 0,
        "exercises_submitted": db.query(func.count(ExerciseResult.id)).scalar() or 0,
        "vocabulary_items": db.query(func.count(Vocabulary.id)).scalar() or 0,
        "grammar_topics": db.query(func.count(GrammarTopic.id)).scalar() or 0,
        "conversations": db.query(func.count(Conversation.id)).scalar() or 0,
    }

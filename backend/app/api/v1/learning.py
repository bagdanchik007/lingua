from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.weakness_service import get_grammar_weaknesses, get_vocabulary_weaknesses
from app.services.streak_service import get_streak, update_streak
from app.services.progress_service import get_user_stats

router = APIRouter(prefix="/learning", tags=["learning"])


@router.get("/path")
def get_learning_path(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Persönlicher Lernpfad: nächste empfohlene Themen + Schwächen."""
    grammar_weak = get_grammar_weaknesses(db, current_user.id, limit=5)
    vocab_weak = get_vocabulary_weaknesses(db, current_user.id, limit=8)
    stats = get_user_stats(db, current_user.id)
    streak = get_streak(db, current_user.id)

    return {
        "stats": stats,
        "streak": streak,
        "grammar_weaknesses": grammar_weak,
        "vocabulary_weaknesses": vocab_weak,
        "recommendation": (
            "Fokussiere dich zuerst auf die Grammatik-Themen mit der niedrigsten Genauigkeit."
            if grammar_weak else
            "Weiter so! Keine starken Schwachstellen erkannt."
        ),
    }


@router.get("/weaknesses")
def get_weaknesses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {
        "grammar": get_grammar_weaknesses(db, current_user.id),
        "vocabulary": get_vocabulary_weaknesses(db, current_user.id),
    }


@router.get("/streak")
def read_streak(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_streak(db, current_user.id)


@router.post("/streak/activity")
def register_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Nach einer Lerneinheit aufrufen, um den Streak zu aktualisieren."""
    streak = update_streak(db, current_user.id)
    return {
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
    }

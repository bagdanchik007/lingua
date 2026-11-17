from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.seed_service import seed_languages_and_levels, seed_grammar_topics

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/seed")
def run_seed(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Seed-Daten für Sprachen, Levels und Grammatik anlegen (nur für Entwicklung)."""
    if not current_user.is_superuser and not current_user.is_active:
        raise HTTPException(status_code=403, detail="Not allowed")

    lang_result = seed_languages_and_levels(db)
    grammar_count = seed_grammar_topics(db)

    return {
        "message": "Seed completed",
        "languages_created": lang_result["languages"],
        "levels_created": lang_result["levels"],
        "grammar_topics_created": grammar_count,
    }

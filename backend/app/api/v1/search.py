from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.models.grammar import GrammarTopic
from app.models.vocabulary import Vocabulary

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/")
def global_search(
    q: str = Query(..., min_length=1, max_length=100),
    language_id: int | None = None,
    limit: int = Query(10, ge=1, le=30),
    db: Session = Depends(get_db),
):
    pattern = f"%{q}%"
    gq = db.query(GrammarTopic).filter(
        GrammarTopic.is_active == True,
        or_(GrammarTopic.title.ilike(pattern), GrammarTopic.slug.ilike(pattern)),
    )
    vq = db.query(Vocabulary).filter(
        Vocabulary.is_active == True,
        or_(Vocabulary.word.ilike(pattern), Vocabulary.translation.ilike(pattern)),
    )
    if language_id:
        gq = gq.filter(GrammarTopic.language_id == language_id)
        vq = vq.filter(Vocabulary.language_id == language_id)

    grammar = gq.limit(limit).all()
    vocab = vq.limit(limit).all()
    return {
        "query": q,
        "grammar": [{"id": g.id, "title": g.title, "slug": g.slug} for g in grammar],
        "vocabulary": [{"id": v.id, "word": v.word, "translation": v.translation} for v in vocab],
    }

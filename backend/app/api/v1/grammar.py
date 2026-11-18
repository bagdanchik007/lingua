from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.models.grammar import GrammarTopic
from app.schemas.grammar import GrammarTopicRead, GrammarTopicCreate
from app.api.deps import get_current_user
from app.models.user import User
from app.utils.exceptions import NotFoundError

router = APIRouter(prefix="/grammar", tags=["grammar"])


@router.get("/", response_model=list[GrammarTopicRead])
def list_grammar_topics(
    language_id: int | None = None,
    level_id: int | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(GrammarTopic).filter(GrammarTopic.is_active == True)
    if language_id:
        query = query.filter(GrammarTopic.language_id == language_id)
    if level_id:
        query = query.filter(GrammarTopic.level_id == level_id)
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                GrammarTopic.title.ilike(pattern),
                GrammarTopic.explanation.ilike(pattern),
            )
        )
    return query.order_by(GrammarTopic.order).all()


@router.get("/search", response_model=list[GrammarTopicRead])
def search_grammar(
    q: str = Query(..., min_length=1),
    language_id: int | None = None,
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    pattern = f"%{q}%"
    query = db.query(GrammarTopic).filter(
        GrammarTopic.is_active == True,
        or_(
            GrammarTopic.title.ilike(pattern),
            GrammarTopic.explanation.ilike(pattern),
            GrammarTopic.slug.ilike(pattern),
        ),
    )
    if language_id:
        query = query.filter(GrammarTopic.language_id == language_id)
    return query.order_by(GrammarTopic.order).limit(limit).all()


@router.get("/{topic_id}", response_model=GrammarTopicRead)
def get_grammar_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(GrammarTopic).filter(GrammarTopic.id == topic_id).first()
    if not topic:
        raise NotFoundError("Grammar topic not found")
    return topic


@router.post("/", response_model=GrammarTopicRead)
def create_grammar_topic(
    data: GrammarTopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topic = GrammarTopic(**data.model_dump())
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic

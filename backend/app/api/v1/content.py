from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.content_import_service import import_vocabulary_items

router = APIRouter(prefix="/content", tags=["content"])


class VocabItemIn(BaseModel):
    word: str
    translation: str
    example_sentence: str | None = None
    example_translation: str | None = None
    word_type: str | None = None
    level_id: int | None = None


class VocabImportIn(BaseModel):
    language_id: int
    items: list[VocabItemIn] = Field(..., min_length=1, max_length=500)


@router.post("/vocabulary/import")
def import_vocab(
    data: VocabImportIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = [i.model_dump() for i in data.items]
    result = import_vocabulary_items(db, data.language_id, items)
    return result

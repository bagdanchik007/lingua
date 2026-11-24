from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.conversation_service import (
    create_conversation,
    list_conversations,
    list_messages,
    send_message,
    get_conversation,
)
from app.utils.rate_limit import ai_rate_limiter

router = APIRouter(prefix="/conversations", tags=["conversations"])


class ConversationCreate(BaseModel):
    language_code: str = "de"
    mode: str = "free"
    title: str | None = None


class ConversationRead(BaseModel):
    id: int
    language_code: str
    mode: str
    title: str | None
    is_active: bool

    model_config = {"from_attributes": True}


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


class MessageRead(BaseModel):
    id: int
    role: str
    content: str

    model_config = {"from_attributes": True}


@router.post("/", response_model=ConversationRead)
def new_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_conversation(
        db, current_user.id, data.language_code, data.mode, data.title
    )


@router.get("/", response_model=list[ConversationRead])
def my_conversations(
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_conversations(db, current_user.id, limit)


@router.get("/{conversation_id}/messages", response_model=list[MessageRead])
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_conversation(db, current_user.id, conversation_id)
    return list_messages(db, conversation_id)


@router.post("/{conversation_id}/messages")
def post_message(
    conversation_id: int,
    data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ai_rate_limiter.check_or_raise(f"ai:conv:{current_user.id}")
    user_msg, assistant_msg = send_message(
        db, current_user.id, conversation_id, data.content
    )
    return {
        "user_message": {"id": user_msg.id, "role": user_msg.role, "content": user_msg.content},
        "assistant_message": {
            "id": assistant_msg.id,
            "role": assistant_msg.role,
            "content": assistant_msg.content,
        },
    }

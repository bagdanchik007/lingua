from sqlalchemy.orm import Session

from app.models.conversation import Conversation, ChatMessage
from app.services.llm.factory import get_llm_provider
from app.services.llm.base import LLMMessage
from app.utils.exceptions import NotFoundError


def create_conversation(
    db: Session,
    user_id: int,
    language_code: str = "de",
    mode: str = "free",
    title: str | None = None,
) -> Conversation:
    conv = Conversation(
        user_id=user_id,
        language_code=language_code,
        mode=mode,
        title=title or f"Chat ({mode})",
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


def get_conversation(db: Session, user_id: int, conversation_id: int) -> Conversation:
    conv = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == user_id)
        .first()
    )
    if not conv:
        raise NotFoundError("Conversation not found")
    return conv


def list_conversations(db: Session, user_id: int, limit: int = 20) -> list[Conversation]:
    return (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
        .all()
    )


def list_messages(db: Session, conversation_id: int, limit: int = 50) -> list[ChatMessage]:
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at.asc())
        .limit(limit)
        .all()
    )


def send_message(
    db: Session,
    user_id: int,
    conversation_id: int,
    content: str,
) -> tuple[ChatMessage, ChatMessage]:
    conv = get_conversation(db, user_id, conversation_id)

    user_msg = ChatMessage(conversation_id=conv.id, role="user", content=content)
    db.add(user_msg)
    db.flush()

    history = list_messages(db, conv.id, limit=20)
    llm_messages = [LLMMessage(role=m.role, content=m.content) for m in history]
    if not any(m.role == "system" for m in llm_messages):
        llm_messages.insert(
            0,
            LLMMessage(
                role="system",
                content=f"Du bist ein geduldiger Sprachlehrer für {conv.language_code}. Modus: {conv.mode}.",
            ),
        )

    provider = get_llm_provider()
    reply = provider.complete(
        llm_messages,
        mode=conv.mode,
        language_code=conv.language_code,
    )

    assistant_msg = ChatMessage(
        conversation_id=conv.id,
        role="assistant",
        content=reply.content,
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(user_msg)
    db.refresh(assistant_msg)
    return user_msg, assistant_msg

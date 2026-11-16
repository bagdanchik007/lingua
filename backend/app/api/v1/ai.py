from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/ai", tags=["ai"])


class ChatMessage(BaseModel):
    message: str
    language_code: str = "de"
    mode: str = "free"  # free | guided | roleplay


class ChatResponse(BaseModel):
    reply: str
    corrections: list[str] = []
    suggestions: list[str] = []


class SpeakingRequest(BaseModel):
    text: str
    language_code: str = "de"


class SpeakingResponse(BaseModel):
    feedback: str
    score: float
    tips: list[str] = []


@router.post("/chat", response_model=ChatResponse)
def ai_chat(
    data: ChatMessage,
    current_user: User = Depends(get_current_user),
):
    """
    KI-Chat Grundgerüst.
    Hier später echte LLM-Anbindung (OpenAI, local model etc.) einbauen.
    """
    # Platzhalter-Antwort
    return ChatResponse(
        reply=f"Das ist eine Platzhalter-Antwort auf: '{data.message}'. "
              f"Hier kommt später die echte KI-Antwort für Sprache '{data.language_code}'.",
        corrections=[],
        suggestions=["Versuche einen längeren Satz zu schreiben.", "Achte auf die Wortstellung."],
    )


@router.post("/speaking", response_model=SpeakingResponse)
def ai_speaking_practice(
    data: SpeakingRequest,
    current_user: User = Depends(get_current_user),
):
    """
    SprechenOrt Grundgerüst.
    Später: Speech-to-Text + Aussprache-Bewertung.
    """
    return SpeakingResponse(
        feedback="Aussprache-Grundgerüst aktiv. Hier kommt später echtes Feedback.",
        score=0.75,
        tips=["Sprich etwas langsamer.", "Achte auf die Betonung der zweiten Silbe."],
    )

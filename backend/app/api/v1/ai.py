from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.api.deps import get_current_user
from app.models.user import User
from app.utils.rate_limit import ai_rate_limiter

router = APIRouter(prefix="/ai", tags=["ai"])


class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    language_code: str = "de"
    mode: str = "free"
    context: str | None = None


class ChatResponse(BaseModel):
    reply: str
    corrections: list[str] = []
    suggestions: list[str] = []
    detected_level: str | None = None
    mode_used: str


class SpeakingRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)
    language_code: str = "de"
    focus: str | None = None


class SpeakingResponse(BaseModel):
    feedback: str
    score: float
    tips: list[str] = []
    detailed_scores: dict = {}


@router.post("/chat", response_model=ChatResponse)
def ai_chat(
    data: ChatMessage,
    request: Request,
    current_user: User = Depends(get_current_user),
):
    client_key = f"ai:chat:{current_user.id}"
    ai_rate_limiter.check_or_raise(client_key)

    mode = data.mode if data.mode in ("free", "guided", "roleplay", "correction") else "free"

    if mode == "correction":
        reply = f"Korrektur-Modus.\nOriginal: „{data.message}“\n(Später echte Korrektur + Erklärung.)"
        corrections = ["Beispiel: Achte auf Artikel und Verbposition."]
        suggestions = ["Formuliere den Satz noch einmal korrigiert."]
    elif mode == "roleplay":
        context = data.context or "Alltag"
        reply = f"Rollenspiel ({context}).\nDu: „{data.message}“\nKI-Antwort folgt mit LLM."
        corrections = []
        suggestions = ["Antworte in vollständigen Sätzen."]
    elif mode == "guided":
        reply = f"Geführter Modus – deine Eingabe: „{data.message}“"
        corrections = []
        suggestions = ["Baue den nächsten Satz etwas aus."]
    else:
        reply = f"Freier Chat ({data.language_code}):\nDu: {data.message}\n— Hier antwortet später das Sprachmodell."
        corrections = []
        suggestions = ["Modi: free, guided, roleplay, correction"]

    return ChatResponse(
        reply=reply,
        corrections=corrections,
        suggestions=suggestions,
        detected_level="A2–B1 (Schätzung)",
        mode_used=mode,
    )


@router.post("/speaking", response_model=SpeakingResponse)
def ai_speaking_practice(
    data: SpeakingRequest,
    current_user: User = Depends(get_current_user),
):
    client_key = f"ai:speaking:{current_user.id}"
    ai_rate_limiter.check_or_raise(client_key)

    return SpeakingResponse(
        feedback=f"SprechenOrt aktiv.\nText: „{data.text[:100]}“\nEchtes Feedback kommt mit Speech-to-Text.",
        score=0.78,
        tips=["Sprich etwas langsamer.", "Achte auf die Wortbetonung.", "Übe schwierige Laute isoliert."],
        detailed_scores={"pronunciation": 0.75, "fluency": 0.80, "grammar": 0.82, "vocabulary": 0.77},
    )

from sqlalchemy.orm import Session

from app.models.audio import SpeakingAttempt
from app.services.llm.factory import get_llm_provider
from app.services.llm.base import LLMMessage


def evaluate_speaking(
    db: Session,
    user_id: int,
    reference_text: str,
    transcript: str | None,
    language_code: str = "de",
) -> SpeakingAttempt:
    """
    Foundation: bewertet anhand Transkript (später STT-Pipeline).
    Ohne Transkript kommt eine neutrale Platzhalter-Bewertung.
    """
    if not transcript:
        score = 0.5
        feedback = "Kein Transkript vorhanden. Bitte Audio später mit Speech-to-Text anbinden."
    else:
        provider = get_llm_provider()
        prompt = (
            f"Bewerte kurz die Aussprache/Nähe zum Referenzsatz auf einer Skala 0-1.\n"
            f"Referenz: {reference_text}\n"
            f"Transkript: {transcript}\n"
            f"Antworte mit: SCORE=<zahl> FEEDBACK=<text>"
        )
        resp = provider.complete(
            [LLMMessage(role="user", content=prompt)],
            language_code=language_code,
        )
        score = 0.7
        feedback = resp.content
        # einfache Score-Extraktion
        if "SCORE=" in resp.content.upper():
            try:
                part = resp.content.upper().split("SCORE=")[1].split()[0]
                score = max(0.0, min(1.0, float(part.replace(",", "."))))
            except Exception:
                pass

    attempt = SpeakingAttempt(
        user_id=user_id,
        language_code=language_code,
        reference_text=reference_text,
        transcript=transcript,
        score=score,
        feedback=feedback,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


def list_attempts(db: Session, user_id: int, limit: int = 20) -> list[SpeakingAttempt]:
    return (
        db.query(SpeakingAttempt)
        .filter(SpeakingAttempt.user_id == user_id)
        .order_by(SpeakingAttempt.created_at.desc())
        .limit(limit)
        .all()
    )

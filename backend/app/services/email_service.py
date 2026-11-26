"""E-Mail Foundation – loggt nur, bis SMTP angebunden ist."""
from app.core.logging import logger


def send_email(to: str, subject: str, body: str) -> bool:
    logger.info("email_stub to=%s subject=%s body=%s", to, subject, body[:200])
    return True


def send_welcome_email(to: str, full_name: str | None = None) -> bool:
    name = full_name or "Lernende/r"
    return send_email(
        to,
        "Willkommen bei LinguaStruct",
        f"Hallo {name},\n\nwillkommen auf der strukturierten Sprachlern-Plattform!\n",
    )


def send_password_reset_stub(to: str, token: str) -> bool:
    return send_email(
        to,
        "Passwort zurücksetzen",
        f"Dein Reset-Token (Stub): {token}\n",
    )

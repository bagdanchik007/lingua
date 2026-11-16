# LinguaStruct

Strukturierte Sprachlern-Plattform mit starkem Fokus auf Grammatik, klaren CEFR-Niveaus und intelligentem Wortschatz-Training.

## Features (aktueller Stand)

- JWT Auth (Register / Login / Me)
- Sprachen & Levels (CEFR + Unterstufen)
- Grammatik-Themen mit Erklärungen
- Wortschatz + Spaced Repetition (SM-2 ähnlich)
- Übungs-Ergebnisse & User-Statistiken
- KI-Chat + SprechenOrt (Grundgerüst / Platzhalter)

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Pydantic v2
- python-jose + passlib (JWT + bcrypt)

## Setup

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# SECRET_KEY und DATABASE_URL anpassen

uvicorn app.main:app --reload
```

API Docs: http://127.0.0.1:8000/docs

## Wichtige Endpunkte

| Methode | Endpunkt | Beschreibung |
|---------|----------|--------------|
| POST | /api/v1/auth/register | Registrierung |
| POST | /api/v1/auth/login | Login (Token) |
| GET | /api/v1/auth/me | Aktueller User |
| GET | /api/v1/languages/ | Sprachen |
| GET | /api/v1/languages/{id}/levels | Levels einer Sprache |
| GET | /api/v1/grammar/ | Grammatik-Themen |
| GET | /api/v1/vocabulary/ | Vokabeln |
| GET | /api/v1/vocabulary/due | Fällige Karten (SRS) |
| POST | /api/v1/vocabulary/review | Karte bewerten |
| POST | /api/v1/progress/exercise | Übungsergebnis speichern |
| GET | /api/v1/progress/stats | User-Statistiken |
| POST | /api/v1/ai/chat | KI-Chat |
| POST | /api/v1/ai/speaking | SprechenOrt |

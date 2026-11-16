# LinguaStruct

**Die strukturierte Sprachlern-Plattform** – Grammatik-first, klare Niveaus und intelligentes Lernen.

LinguaStruct ist eine moderne Alternative zu klassischen Sprach-Apps. Statt nur gamifizierter Mini-Übungen setzen wir auf systematischen Grammatik-Aufbau, echte Erklärungen und adaptive Wiederholung.

---

## Vision

Eine Lernplattform, die:

- Klare und nachvollziehbare Niveaustufen bietet (CEFR + Unterstufen)
- Grammatik endlich richtig erklärt
- Wortschatz intelligent wiederholt (Spaced Repetition)
- Mit KI sprechen und chatten lässt
- Später echte Gespräche mit anderen Lernenden ermöglicht

**Zielsprachen (geplant):**
- Deutsch ↔ Englisch
- Deutsch ↔ Französisch
- Italienisch, Spanisch, Russisch

---

## Features

### Aktuell verfügbar
- Benutzer-System mit JWT-Authentifizierung
- Sprachen & Level-Verwaltung (CEFR-basiert)
- Grammatik-Themen mit ausführlichen Erklärungen
- Wortschatz-Modul inkl. Spaced-Repetition-System
- Übungs-Tracking & persönliche Statistiken
- KI-Chat & SprechenOrt (Grundgerüst)

### In Planung / Nächste Ausbaustufen
- Adaptive Schwierigkeitsanpassung
- Schwachstellen-Analyse („Du hast Probleme mit dem Konjunktiv II“)
- Echte KI-Gespräche (LLM-Anbindung)
- Aussprache-Training mit Speech-to-Text
- Gespräche mit echten Usern (Matching)
- Detaillierte Lernpfade pro Sprache
- Admin-Bereich für Content-Management

---

## Tech Stack

| Bereich              | Technologie              |
|----------------------|--------------------------|
| Backend              | Python, FastAPI          |
| Datenbank            | PostgreSQL + SQLAlchemy 2.0 |
| Authentifizierung    | JWT + OAuth2             |
| Validierung          | Pydantic v2              |
| Spaced Repetition    | Eigenes SM-2-ähnliches System |
| KI (geplant)         | OpenAI / lokale Modelle  |
| Migrationen          | Alembic                  |

---

## Projektstruktur

```text
linguastruct/
├── app/
│   ├── api/v1/          # Alle API-Endpunkte
│   ├── core/            # Config, Security, Database
│   ├── models/          # SQLAlchemy Models
│   ├── schemas/         # Pydantic Schemas
│   ├── services/        # Business Logic
│   └── main.py
├── alembic/             # Datenbank-Migrationen
├── tests/
├── requirements.txt
└── README.md

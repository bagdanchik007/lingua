# LinguaStruct

Strukturierte Sprachlern-Plattform mit starkem Fokus auf Grammatik, klaren Niveaus und intelligentem Wortschatz-Training.

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Pydantic Settings
- Alembic (Migrationen)

## Projekt starten

```bash
# Virtuelle Umgebung erstellen
python -m venv venv

# Aktivieren
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# .env Datei erstellen
cp .env.example .env
# Dann DATABASE_URL und SECRET_KEY anpassen

# Server starten
uvicorn app.main:app --reload
```

API Dokumentation: http://127.0.0.1:8000/docs

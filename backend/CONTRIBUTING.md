# Contributing to LinguaStruct

## Conventional Commits

- `feat:` neue Funktion
- `fix:` Bugfix
- `refactor:` Umbau ohne Feature/Fix
- `docs:` Dokumentation
- `chore:` Wartung
- `test:` Tests
- `build:` Dependencies / Build

## Entwicklung

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Struktur

Business-Logik liegt in `app/services/`.  
Router bleiben dünn.

"""Einmalig Tabellen anlegen (ohne Alembic). Nur für lokale Entwicklung."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.models import *  # noqa: F401,F403


def main() -> None:
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")


if __name__ == "__main__":
    main()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import auth, languages, grammar, vocabulary, progress, ai, admin, learning

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Alle Router einbinden
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(languages.router, prefix=settings.API_V1_STR)
app.include_router(grammar.router, prefix=settings.API_V1_STR)
app.include_router(vocabulary.router, prefix=settings.API_V1_STR)
app.include_router(progress.router, prefix=settings.API_V1_STR)
app.include_router(ai.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)
app.include_router(learning.router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "message": "Willkommen bei LinguaStruct API",
        "docs": "/docs",
        "version": "0.4.0",
        "features": [
            "Auth (Register/Login/JWT)",
            "Languages & Levels (CEFR)",
            "Grammar Topics mit echten Erklärungen",
            "Vocabulary + Spaced Repetition",
            "Progress, Stats & Streaks",
            "Weakness Detection & Learning Path",
            "AI Chat (free/guided/roleplay/correction)",
            "SprechenOrt Foundation",
            "Seed Data für Sprachen & Grammatik",
        ],
    }


@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.4.0"}

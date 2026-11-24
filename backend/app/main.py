from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.middleware.request_id import RequestIdMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.api.v1 import (
    auth, users, languages, grammar, vocabulary,
    progress, ai, admin, learning, exercises, dashboard,
    achievements, notifications, leaderboard, search, feedback,
    sessions, favorites, reports,
    conversations, lessons, social, adaptive,
)

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    version="1.0.0",
    contact={"name": "LinguaStruct", "email": "dev@linguastruct.local"},
    license_info={"name": "MIT"},
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (
    auth.router, users.router, languages.router, grammar.router,
    vocabulary.router, progress.router, ai.router, admin.router,
    learning.router, exercises.router, dashboard.router,
    achievements.router, notifications.router, leaderboard.router,
    search.router, feedback.router, sessions.router, favorites.router,
    reports.router, conversations.router, lessons.router,
    social.router, adaptive.router,
):
    app.include_router(router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "message": "Willkommen bei LinguaStruct API",
        "docs": "/docs",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/ready")
def readiness_check():
    return {"status": "ready"}


@app.get("/version")
def version_info():
    return {"version": "1.0.0", "project": settings.PROJECT_NAME}

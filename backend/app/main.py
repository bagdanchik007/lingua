from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.middleware.request_id import RequestIdMiddleware
from app.api.v1 import (
    auth, users, languages, grammar, vocabulary,
    progress, ai, admin, learning, exercises, dashboard,
)

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    version="0.7.0",
)

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
):
    app.include_router(router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "message": "Willkommen bei LinguaStruct API",
        "docs": "/docs",
        "version": "0.7.0",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.7.0"}


@app.get("/ready")
def readiness_check():
    return {"status": "ready"}

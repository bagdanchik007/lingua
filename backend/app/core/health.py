from sqlalchemy import text
from app.core.database import engine
from app.services.redis_cache import redis_cache


def check_database() -> dict:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "up"}
    except Exception as exc:
        return {"status": "down", "error": str(exc)[:200]}


def check_redis() -> dict:
    if redis_cache.using_redis:
        try:
            redis_cache.set("healthcheck", "1", ttl=5)
            return {"status": "up"}
        except Exception as exc:
            return {"status": "down", "error": str(exc)[:200]}
    return {"status": "disabled"}


def full_health() -> dict:
    return {
        "status": "ok",
        "database": check_database(),
        "redis": check_redis(),
    }

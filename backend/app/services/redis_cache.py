"""
Optional Redis-Cache.
Wenn REDIS_URL nicht gesetzt ist, fällt alles auf In-Memory TTLCache zurück.
"""
import os
from typing import Any

from app.utils.cache import app_cache, TTLCache


class RedisCacheAdapter:
    def __init__(self) -> None:
        self._client = None
        url = os.getenv("REDIS_URL")
        if url:
            try:
                import redis  # type: ignore

                self._client = redis.Redis.from_url(url, decode_responses=True)
                self._client.ping()
            except Exception:
                self._client = None
        self._fallback = app_cache

    @property
    def using_redis(self) -> bool:
        return self._client is not None

    def get(self, key: str) -> Any | None:
        if not self._client:
            return self._fallback.get(key)
        val = self._client.get(key)
        return val

    def set(self, key: str, value: str, ttl: int = 60) -> None:
        if not self._client:
            self._fallback.set(key, value, ttl=ttl)
            return
        self._client.setex(key, ttl, value)


redis_cache = RedisCacheAdapter()

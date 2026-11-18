"""
Einfaches In-Memory Rate Limiting (Foundation).
Für Produktion später durch Redis ersetzen.
"""
from collections import defaultdict
from time import time
from fastapi import HTTPException, status


class RateLimiter:
    def __init__(self, max_calls: int = 60, period_seconds: int = 60):
        self.max_calls = max_calls
        self.period = period_seconds
        self._calls: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        now = time()
        window_start = now - self.period
        # Alte Einträge entfernen
        self._calls[key] = [t for t in self._calls[key] if t > window_start]
        if len(self._calls[key]) >= self.max_calls:
            return False
        self._calls[key].append(now)
        return True

    def check_or_raise(self, key: str) -> None:
        if not self.is_allowed(key):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Bitte später erneut versuchen.",
            )


# Globale Instanzen
ai_rate_limiter = RateLimiter(max_calls=30, period_seconds=60)
api_rate_limiter = RateLimiter(max_calls=120, period_seconds=60)

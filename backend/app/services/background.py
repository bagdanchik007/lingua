"""Sehr einfache Hintergrund-Aufgaben (synchroner Stub)."""
from collections.abc import Callable
from typing import Any

from app.core.logging import logger


def enqueue(task_name: str, fn: Callable[..., Any], *args, **kwargs) -> Any:
    """
    Später: Celery / RQ / ARQ.
    Aktuell: sofort ausführen und loggen.
    """
    logger.info("background_task start name=%s", task_name)
    try:
        result = fn(*args, **kwargs)
        logger.info("background_task done name=%s", task_name)
        return result
    except Exception:
        logger.exception("background_task failed name=%s", task_name)
        raise

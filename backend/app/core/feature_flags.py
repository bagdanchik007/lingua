"""Einfache Feature Flags aus Environment / Settings."""
from app.core.config import settings


class FeatureFlags:
    @property
    def ai_enabled(self) -> bool:
        return settings.ENVIRONMENT != "production_locked"

    @property
    def leaderboard_enabled(self) -> bool:
        return True

    @property
    def achievements_enabled(self) -> bool:
        return True

    @property
    def reports_enabled(self) -> bool:
        return True


flags = FeatureFlags()

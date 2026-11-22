from datetime import datetime
from pydantic import BaseModel


class AchievementRead(BaseModel):
    id: int
    code: str
    title: str
    description: str
    icon: str | None = None
    xp_reward: int

    model_config = {"from_attributes": True}


class UserAchievementRead(BaseModel):
    id: int
    achievement_id: int
    unlocked_at: datetime
    achievement: AchievementRead | None = None

    model_config = {"from_attributes": True}

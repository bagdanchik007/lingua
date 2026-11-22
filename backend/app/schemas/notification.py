from datetime import datetime
from pydantic import BaseModel


class NotificationRead(BaseModel):
    id: int
    title: str
    body: str
    category: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationCreate(BaseModel):
    title: str
    body: str
    category: str = "system"

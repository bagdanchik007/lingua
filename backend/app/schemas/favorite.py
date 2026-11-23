from datetime import datetime
from pydantic import BaseModel


class FavoriteCreate(BaseModel):
    vocabulary_id: int


class FavoriteRead(BaseModel):
    id: int
    vocabulary_id: int
    created_at: datetime

    model_config = {"from_attributes": True}

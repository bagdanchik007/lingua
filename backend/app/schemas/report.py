from datetime import datetime
from pydantic import BaseModel, Field


class ContentReportCreate(BaseModel):
    target_type: str = Field(..., pattern="^(grammar|vocabulary|exercise)$")
    target_id: int
    reason: str = Field(..., min_length=3, max_length=100)
    details: str | None = Field(default=None, max_length=2000)


class ContentReportRead(BaseModel):
    id: int
    target_type: str
    target_id: int
    reason: str
    details: str | None
    is_resolved: bool
    created_at: datetime

    model_config = {"from_attributes": True}

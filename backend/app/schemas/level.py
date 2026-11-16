from pydantic import BaseModel


class LevelBase(BaseModel):
    code: str
    name: str
    description: str | None = None
    order: int = 0
    cefr_level: str
    is_active: bool = True


class LevelCreate(LevelBase):
    language_id: int


class LevelRead(LevelBase):
    id: int
    language_id: int

    model_config = {"from_attributes": True}

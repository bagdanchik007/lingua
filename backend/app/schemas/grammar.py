from pydantic import BaseModel


class GrammarTopicBase(BaseModel):
    title: str
    slug: str
    explanation: str
    examples: str | None = None
    order: int = 0
    is_active: bool = True


class GrammarTopicCreate(GrammarTopicBase):
    language_id: int
    level_id: int


class GrammarTopicRead(GrammarTopicBase):
    id: int
    language_id: int
    level_id: int

    model_config = {"from_attributes": True}

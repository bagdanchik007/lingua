from pydantic import BaseModel


class LanguageBase(BaseModel):
    code: str
    name: str
    name_en: str
    is_active: bool = True


class LanguageCreate(LanguageBase):
    pass


class LanguageRead(LanguageBase):
    id: int

    model_config = {"from_attributes": True}

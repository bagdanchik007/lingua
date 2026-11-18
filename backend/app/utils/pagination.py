from typing import Generic, TypeVar, Sequence
from pydantic import BaseModel, Field

T = TypeVar("T")


class PageParams(BaseModel):
    skip: int = Field(0, ge=0, description="Anzahl zu überspringender Einträge")
    limit: int = Field(20, ge=1, le=100, description="Maximale Anzahl Einträge")


class Page(BaseModel, Generic[T]):
    items: Sequence[T]
    total: int
    skip: int
    limit: int
    has_more: bool

    @classmethod
    def create(cls, items: Sequence[T], total: int, skip: int, limit: int) -> "Page[T]":
        return cls(
            items=items,
            total=total,
            skip=skip,
            limit=limit,
            has_more=(skip + len(items)) < total,
        )

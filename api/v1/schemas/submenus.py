from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    id: UUID


class SubmenuDetail(SubmenuCreate):
    dishes_count: int


class SubmenuList(BaseModel):
    __root__: list[SubmenuDetail]


class SubmenuUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]

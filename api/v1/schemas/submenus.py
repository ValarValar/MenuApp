from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    id: UUID


class SubmenuWithCount(SubmenuCreate):
    dishes_count: int


class SubmenuUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]

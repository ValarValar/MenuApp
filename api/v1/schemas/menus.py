from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    id: UUID


class MenuWithCount(MenuCreate):
    submenus_count: int
    dishes_count: int


class MenuUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]

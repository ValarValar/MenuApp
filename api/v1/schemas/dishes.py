from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str
    price: str


class DishList(BaseModel):
    __root__: list[DishBase]


class DishCreate(DishBase):
    id: UUID


class DishUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[str]

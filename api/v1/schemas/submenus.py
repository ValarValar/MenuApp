from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuForCreate(SubmenuBase):
    menu_id: UUID


class SubmenuCreate(SubmenuBase):
    id: UUID


class SubmenuUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]

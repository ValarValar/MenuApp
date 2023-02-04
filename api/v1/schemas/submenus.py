from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: str

    class Config:
        schema_extra = {
            "example": {
                "title": "My submenu 1",
                "description": "My submenu description 1",
            },
        }


class SubmenuCreate(SubmenuBase):
    id: UUID

    class Config:
        schema_extra = {
            "example": {
                "id": "8bfd01b6-2a5e-4a91-b5aa-00adeb3780a0",
                "title": "My submenu 1",
                "description": "My submenu description 1",
            },
        }


class SubmenuDetail(SubmenuCreate):
    dishes_count: int

    class Config:
        schema_extra = {
            "example": {
                "id": "8bfd01b6-2a5e-4a91-b5aa-00adeb3780a0",
                "title": "My detailed submenu 1",
                "description": "My detailed submenu description 1",
                "dishes_count": 3,
            },
        }


class SubmenuList(BaseModel):
    __root__: list[SubmenuDetail]

    class Config:
        schema_extra = {
            "example": [
                {
                    "id": "8bfd01b6-2a5e-4a91-b5aa-00adeb3780a0",
                    "title": "My detailed submenu 1",
                    "description": "My detailed submenu description 1",
                    "dishes_count": 3,
                },
                {
                    "id": "8bfd01b6-2a5e-4a91-b5aa-00adeb3780a1",
                    "title": "My detailed submenu 1",
                    "description": "My detailed submenu description 1",
                    "dishes_count": 1,
                },
            ],
        }


class SubmenuUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]

    class Config:
        schema_extra = {
            "example_1": {
                "title": "My updated submenu 1",
            },
            "example_2": {
                "description": "My updated submenu description 1",
            },
            "example_3": {
                "title": "My updated menu 1",
                "description": "My updated submenu description 1",
            },
        }

from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID


class MenuBase(BaseModel):
    title: str
    description: str

    class Config:
        schema_extra = {
            'example': {
                'title': 'My menu 1',
                'description': 'My menu description 1',
            },
        }


class MenuCreate(MenuBase):
    id: UUID

    class Config:
        schema_extra = {
            'example': {
                'id': '8bfd01b6-2a5e-4a91-b5aa-00adeb3780a0',
                'title': 'My menu 1',
                'description': 'My menu description 1',
            },
        }


class MenuDetail(MenuCreate):
    submenus_count: int
    dishes_count: int

    class Config:
        schema_extra = {
            'example': {
                'id': '8bfd01b6-2a5e-4a91-b5aa-00adeb3780a0',
                'title': 'My detailed menu 1',
                'description': 'My detailed menu description 1',
                'submenus_count': 2,
                'dishes_count': 3,
            },
        }


class MenuList(BaseModel):
    __root__: list[MenuDetail]

    class Config:
        schema_extra = {
            'example': [
                {
                    'id': '8bfd01b6-2a5e-4a91-b5aa-00adeb3780a0',
                    'title': 'My detailed menu 1',
                    'description': 'My detailed menu description 1',
                    'submenus_count': 2,
                    'dishes_count': 3,
                },
                {
                    'id': '8bfd01b6-2a5e-4a91-b5aa-00adeb3780a1',
                    'title': 'My detailed menu 1',
                    'description': 'My detailed menu description 1',
                    'submenus_count': 2,
                    'dishes_count': 1,
                },
            ],

        }


class MenuUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]

    class Config:
        schema_extra = {
            'example_1': {
                'title': 'My updated menu 1',
            },
            'example_2': {
                'description': 'My updated menu description 1',
            },
            'example_3': {
                'title': 'My updated menu 1',
                'description': 'My updated menu description 1',
            },
        }

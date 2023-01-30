from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str
    price: str

    class Config:
        schema_extra = {
            'example': {
                'title': 'My dish 1',
                'description': 'My dish description 1',
                'price': '12.50',
            },
        }


class DishList(BaseModel):
    __root__: list[DishBase]

    class Config:
        schema_extra = {
            'example_1': [
                {
                    'title': 'My dish 1',
                    'description': 'My dish description 1',
                    'price': '12.50',
                },
                {
                    'title': 'My dish 2',
                    'description': 'My dish description 2',
                    'price': '13.50',
                },
            ],
            'example_2': [],
        }


class DishCreate(DishBase):
    id: UUID

    class Config:
        schema_extra = {
            'example': {
                'id': '8bfd01b6-2a5e-4a91-b5aa-00adeb3780a0',
                'title': 'My updated dish 1',
                'description': 'My updated dish description 1',
                'price': '12.55',
            },
        }


class DishUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[str]

    class Config:
        schema_extra = {
            'example_1': {
                'title': 'My updated dish 1',
                'description': 'My updated dish description 1',
                'price': '12.55',
            },
            'example_2': {
                'title': 'My updated dish 1',
                'price': '12.55',
            },
        }

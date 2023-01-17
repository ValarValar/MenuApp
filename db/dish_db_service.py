from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlmodel import Session

from api.v1.schemas.dishes import DishUpdate, DishBase
from db.db import get_session
from db.mixin_db_service import CRUDDBServiceMixin
from models import Dish


class DishDbService(CRUDDBServiceMixin):
    def __init__(self, session: Session):
        super().__init__(session, Dish)

    def create_item(self, dish: DishBase) -> Dish:
        return super().create_item(dish)

    def list_items(self) -> list[Dish]:
        return super().list_items()

    def get_item_by_id(self, id: str) -> Optional[Dish]:
        return super().get_item_by_id(id)

    def update_item(self, id: str, update_dish: DishUpdate) -> Optional[Dish]:
        return super().update_item(id, update_dish)

    def delete_item(self, id: str) -> bool:
        return super().delete_item(id)


@lru_cache
def get_dish_db_service(session: Session = Depends(get_session)) -> DishDbService:
    return DishDbService(session)

from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlmodel import Session, select

from api.v1.schemas.dishes import DishBase, DishUpdate
from db.db import get_session
from db.mixin import ServiceMixin
from models import Dish, Submenu


class DishDbService(ServiceMixin):
    def create_dish(self, dish: DishBase, submenu_id: str) -> Dish:
        new_dish = Dish(submenu_id=submenu_id, **dish.dict())
        self.session.add(new_dish)
        self.session.commit()
        self.session.refresh(new_dish)
        return new_dish

    def list_dishes(self, menu_id: str, submenu_id: str) -> list[Dish]:
        statement = select(Dish).join(Submenu)\
            .where(Dish.submenu_id == submenu_id)\
            .where(Submenu.menu_id == menu_id)
        results = self.session.exec(statement).all()
        return results

    def get_dish_by_ids(self, menu_id: str, submenu_id: str, dish_id: str) -> Optional[Dish]:
        statement = select(Dish).join(Submenu) \
            .where(Dish.submenu_id == submenu_id)\
            .where(Submenu.menu_id == menu_id) \
            .where(Dish.id == dish_id)
        results = self.session.exec(statement).first()
        return results


    def update_dish(self, menu_id: str, submenu_id: str, dish_id: str, update_submenu: DishUpdate) -> Optional[Dish]:
        current_dish = self.get_dish_by_ids(menu_id, submenu_id, dish_id)
        if current_dish:
            update_menu = update_submenu.dict(exclude_unset=True)
            for key, value in update_menu.items():
                setattr(current_dish, key, value)
            self.session.add(current_dish)
            self.session.commit()
            self.session.refresh(current_dish)
        return current_dish

    def delete_dish(self, menu_id: str, submenu_id: str, dish_id: str, ) -> bool:
        current_dish = self.get_dish_by_ids(menu_id, submenu_id, dish_id)
        if current_dish:
            self.session.delete(current_dish)
            self.session.commit()
            return True
        return False


@lru_cache
def get_dish_db_service(session: Session = Depends(get_session)) -> DishDbService:
    return DishDbService(session)

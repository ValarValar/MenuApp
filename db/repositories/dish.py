from typing import Optional

from sqlmodel import select

from api.v1.schemas.dishes import DishBase, DishUpdate
from db.repositories.base import AbstractRepository
from models import Dish, Submenu


class DishRepository(AbstractRepository):
    def create(self, dish: DishBase, submenu_id: str) -> Dish:
        new_dish = Dish(submenu_id=submenu_id, **dish.dict())
        self.session.add(new_dish)
        return new_dish

    def list(self, menu_id: str, submenu_id: str) -> list[Dish]:
        statement = select(Dish).join(Submenu).where(
            Dish.submenu_id == submenu_id
        ).where(
            Submenu.menu_id == menu_id
        )
        results = self.session.exec(statement).all()
        return results

    def get(self, menu_id: str, submenu_id: str, dish_id: str) -> Optional[Dish]:
        statement = select(Dish).join(Submenu).where(
            Dish.submenu_id == submenu_id
        ).where(
            Submenu.menu_id == menu_id
        ).where(
            Dish.id == dish_id
        )
        detailed_dish = self.session.exec(statement).first()
        return detailed_dish

    def update(
            self,
            menu_id: str,
            submenu_id: str,
            dish_id: str,
            update_submenu: DishUpdate
    ) -> Dish:
        current_dish = self.get(menu_id, submenu_id, dish_id)
        if current_dish:
            update_menu = update_submenu.dict(exclude_unset=True)
            for key, value in update_menu.items():
                setattr(current_dish, key, value)
            self.session.add(current_dish)
        return current_dish

    def delete(self, menu_id: str, submenu_id: str, dish_id: str) -> bool:
        current_dish = self.get(menu_id, submenu_id, dish_id)
        if current_dish:
            self.session.delete(current_dish)
            return True
        return False

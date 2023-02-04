from typing import Optional

from sqlalchemy import select

from api.v1.schemas.dishes import DishBase, DishUpdate
from db.repositories.base import AbstractRepository
from models import Dish, Submenu


class DishRepository(AbstractRepository):
    async def create(self, dish: DishBase, submenu_id: str) -> Dish:
        new_dish = Dish(submenu_id=submenu_id, **dish.dict())
        self.session.add(new_dish)
        return new_dish

    async def list(self, menu_id: str, submenu_id: str) -> list[Dish]:
        statement = (
            select(
                Dish.id,
                Dish.description,
                Dish.title,
                Dish.price,
            )
            .join(Submenu)
            .where(
                Dish.submenu_id == submenu_id,
            )
            .where(
                Submenu.menu_id == menu_id,
            )
        )
        results = await self.session.execute(statement)
        dishes: list[Dish] = results.all()
        return dishes

    async def get(self, menu_id: str, submenu_id: str, dish_id: str) -> Optional[Dish]:
        statement = (
            select(
                Dish,
            )
            .join(Submenu)
            .where(
                Dish.submenu_id == submenu_id,
            )
            .where(
                Submenu.menu_id == menu_id,
            )
            .where(
                Dish.id == dish_id,
            )
        )
        results = await self.session.execute(statement)
        detailed_dish: Optional[Dish] = results.scalar_one_or_none()
        return detailed_dish

    async def update(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        update_submenu: DishUpdate,
    ) -> Optional[Dish]:
        if current_dish := await self.get(menu_id, submenu_id, dish_id):
            update_menu = update_submenu.dict(exclude_unset=True)
            for key, value in update_menu.items():
                setattr(current_dish, key, value)
            self.session.add(current_dish)
        return current_dish

    async def delete(self, menu_id: str, submenu_id: str, dish_id: str) -> bool:
        if current_dish := await self.get(menu_id, submenu_id, dish_id):
            await self.session.delete(current_dish)
            return True
        return False

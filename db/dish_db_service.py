from functools import lru_cache
from typing import Optional

from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from api.v1.schemas.dishes import DishBase, DishUpdate, DishCreate
from db.cache.base import AbstractCache, get_cache
from db.db import get_session
from db.menu_db_service import MenuDbService
from db.mixin import ServiceMixin
from db.submenu_db_service import SubmenuDbService, get_submenu_db_service
from db.uow import SqlModelUnitOfWork
from models import Dish, Submenu


class DishDbService(ServiceMixin):
    @staticmethod
    def submenu_exists(menu_id: str, submenu_id: str) -> None:
        """
        Checks that submenu with submenu_id exists inside menu with menu_id,
        if not raises an exception
        :param menu_id:
        :param submenu_id:
        :return: None
        """
        #submenu = submenu_db.get_submenu_by_ids(menu_id, submenu_id)
        #if not submenu:
        #    raise HTTPException(status_code=404, detail="submenu not found")

    def create_dish(self, dish: DishBase, menu_id: str, submenu_id: str) -> DishCreate:
        self.submenu_exists(menu_id, submenu_id)

        new_dish = Dish(submenu_id=submenu_id, **dish.dict())
        self.session.add(new_dish)
        self.session.commit()
        self.session.refresh(new_dish)

        return DishCreate(**new_dish.dict())

    def list_dishes(self, menu_id: str, submenu_id: str) -> list[DishBase]:
        self.submenu_exists(menu_id, submenu_id)

        statement = select(Dish).join(Submenu) \
            .where(Dish.submenu_id == submenu_id) \
            .where(Submenu.menu_id == menu_id)
        results = self.session.exec(statement).all()

        dishes = [DishBase(**dish.dict()) for dish in results]
        return dishes

    def get_dish_by_ids(self, menu_id: str, submenu_id: str, dish_id: str) -> Optional[DishCreate]:
        statement = select(Dish).join(Submenu) \
            .where(Dish.submenu_id == submenu_id) \
            .where(Submenu.menu_id == menu_id) \
            .where(Dish.id == dish_id)
        detailed_dish = self.session.exec(statement).first()

        if not detailed_dish:
            raise HTTPException(status_code=404, detail="dish not found")
        return DishCreate(**detailed_dish.dict())

    def update_dish(self, menu_id: str, submenu_id: str, dish_id: str, update_submenu: DishUpdate) -> Optional[DishCreate]:
        current_dish = self.get_dish_by_ids(menu_id, submenu_id, dish_id)
        if current_dish:
            update_menu = update_submenu.dict(exclude_unset=True)
            for key, value in update_menu.items():
                setattr(current_dish, key, value)
            self.session.add(current_dish)
            self.session.commit()
            self.session.refresh(current_dish)


        if not current_dish:
            raise HTTPException(status_code=404, detail="dish not found")
        return DishCreate(**current_dish.dict())

    def delete_dish(self, menu_id: str, submenu_id: str, dish_id: str, ) -> dict:
        current_dish = self.get_dish_by_ids(menu_id, submenu_id, dish_id)
        if current_dish:
            self.session.delete(current_dish)
            self.session.commit()
            return {"deleted": True}
        raise HTTPException(status_code=404, detail="dish not found")


@lru_cache
def get_dish_db_service(
        cache: AbstractCache = Depends(get_cache),
        session: Session = Depends(get_session)
) -> MenuDbService:
    uow = SqlModelUnitOfWork(session)
    return MenuDbService(cache=cache, uow=uow)

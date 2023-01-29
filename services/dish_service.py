from functools import lru_cache
from typing import Optional

from fastapi import Depends, HTTPException
from sqlmodel import Session

from api.v1.schemas.dishes import DishBase, DishUpdate, DishCreate, DishList
from db.cache.base import AbstractCache, get_cache
from db.db import get_session
from services.mixin import ServiceMixin
from db.uow import SqlModelUnitOfWork


class DishService(ServiceMixin):

    def submenu_exists(self, menu_id: str, submenu_id: str) -> None:
        """
        Checks that submenu with submenu_id exists inside menu with menu_id,
        if not raises an exception
        :param menu_id:
        :param submenu_id:
        :return: None
        """
        with self.uow:
            submenu = self.uow.submenu_repo.get_by_ids(menu_id, submenu_id)
            if not submenu:
                raise HTTPException(status_code=404, detail="submenu not found")
        return

    def create(self, dish: DishBase, menu_id: str, submenu_id: str) -> DishCreate:
        self.submenu_exists(menu_id, submenu_id)
        with self.uow:
            new_dish = self.uow.dish_repo.create(dish, submenu_id)
            response = DishCreate(**new_dish.dict())
        return response

    def list(self, menu_id: str, submenu_id: str) -> DishList:
        self.submenu_exists(menu_id, submenu_id)

        with self.uow:
            dishes = self.uow.dish_repo.list(menu_id, submenu_id)
            response = DishList.parse_obj(dishes)
        return response

    def get(self, menu_id: str, submenu_id: str, dish_id: str) -> Optional[DishCreate]:
        with self.uow:
            dish = self.uow.dish_repo.get(menu_id, submenu_id, dish_id)
            if not dish:
                raise HTTPException(status_code=404, detail="dish not found")
            response = DishCreate(**dish.dict())
        return response

    def update(
            self,
            menu_id: str,
            submenu_id: str,
            dish_id: str,
            update_submenu: DishUpdate
    ) -> Optional[DishCreate]:
        with self.uow:
            dish = self.uow.dish_repo.update(menu_id, submenu_id, dish_id, update_submenu)
            if not dish:
                raise HTTPException(status_code=404, detail="dish not found")
            response = DishCreate(**dish.dict())
        return response

    def delete(self, menu_id: str, submenu_id: str, dish_id: str) -> dict:
        with self.uow:
            deleted = self.uow.dish_repo.delete(menu_id, submenu_id, dish_id)
        if deleted:
            return {"deleted": deleted}
        else:
            raise HTTPException(status_code=404, detail="dish not found")


@lru_cache
def get_dish_service(
        cache: AbstractCache = Depends(get_cache),
        session: Session = Depends(get_session)
) -> DishService:
    uow = SqlModelUnitOfWork(session)
    return DishService(cache=cache, uow=uow)

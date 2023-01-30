from functools import lru_cache
from typing import Optional

from fastapi import Depends, HTTPException
from sqlmodel import Session

from api.v1.schemas.dishes import DishBase, DishCreate, DishList, DishUpdate
from db.cache.base import AbstractCache
from db.cache.RedisCache import get_redis_cache
from db.db import get_session
from db.uow import SqlModelUnitOfWork
from services.mixin import ServiceMixin


class DishService(ServiceMixin):
    list_cache_key = 'dish-list'

    def clear_cache(self, menu_id: str = '', submenu_id: str = '', dish_id: str = ''):
        self.cache.delete(menu_id)
        self.cache.delete(submenu_id)
        self.cache.delete(dish_id)
        self.cache.delete(self.list_cache_key)

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
                raise HTTPException(
                    status_code=404, detail='submenu not found',
                )
        return

    def create(self, dish: DishBase, menu_id: str, submenu_id: str) -> DishCreate:
        self.submenu_exists(menu_id, submenu_id)

        with self.uow:
            new_dish = self.uow.dish_repo.create(dish, submenu_id)
            response = DishCreate(**new_dish.dict())
        self.clear_cache(menu_id, submenu_id)
        return response

    def get_list(self, menu_id: str, submenu_id: str) -> DishList:
        # self.submenu_exists(menu_id, submenu_id) commented for postman test pass

        cache_value = self.cache.get(self.list_cache_key)
        if cache_value:
            return DishList.parse_raw(cache_value)

        with self.uow:
            dishes = self.uow.dish_repo.list(menu_id, submenu_id)
            response = DishList.parse_obj(dishes)

        self.cache.set(self.list_cache_key, response.json())
        return response

    def get_detail(self, menu_id: str, submenu_id: str, dish_id: str) -> Optional[DishCreate]:
        cache_value = self.cache.get(dish_id)
        if cache_value:
            return DishCreate.parse_raw(cache_value)

        with self.uow:
            dish = self.uow.dish_repo.get(menu_id, submenu_id, dish_id)
            if not dish:
                raise HTTPException(status_code=404, detail='dish not found')
            response = DishCreate(**dish.dict())

        self.cache.set(dish_id, response.json())
        return response

    def update(
            self,
            menu_id: str,
            submenu_id: str,
            dish_id: str,
            update_submenu: DishUpdate,
    ) -> Optional[DishCreate]:
        with self.uow:
            dish = self.uow.dish_repo.update(
                menu_id, submenu_id, dish_id, update_submenu,
            )
            if not dish:
                raise HTTPException(status_code=404, detail='dish not found')
            response = DishCreate(**dish.dict())
        self.clear_cache(menu_id, submenu_id, dish_id)
        return response

    def delete(self, menu_id: str, submenu_id: str, dish_id: str) -> dict:
        with self.uow:
            deleted = self.uow.dish_repo.delete(menu_id, submenu_id, dish_id)
        self.clear_cache(menu_id, submenu_id, dish_id)
        if deleted:
            return {'deleted': deleted}
        else:
            raise HTTPException(status_code=404, detail='dish not found')


@lru_cache
def get_dish_service(
        cache: AbstractCache = Depends(get_redis_cache),
        session: Session = Depends(get_session),
) -> DishService:
    uow = SqlModelUnitOfWork(session)
    return DishService(cache=cache, uow=uow)

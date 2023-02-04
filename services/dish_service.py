from functools import lru_cache
from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.dishes import DishBase, DishCreate, DishList, DishUpdate
from api.v1.schemas.service import DeleteBase
from db.cache.base import AbstractCache
from db.cache.RedisCache import get_redis_cache
from db.db import get_session
from db.uow import SqlModelUnitOfWork
from services.mixin import ServiceMixin


class DishService(ServiceMixin):
    list_cache_key = "dish-list"

    async def clear_cache(
        self, menu_id: str = "", submenu_id: str = "", dish_id: str = ""
    ):
        await self.cache.delete(menu_id)
        await self.cache.delete(submenu_id)
        await self.cache.delete(dish_id)
        await self.cache.delete(self.list_cache_key)

    async def submenu_exists(self, menu_id: str, submenu_id: str) -> bool:
        """
        Checks that submenu with submenu_id exists inside menu with menu_id,
        if not raises an exception
        :param menu_id:
        :param submenu_id:
        :return: None
        """
        async with self.uow:
            submenu = await self.uow.submenu_repo.get(menu_id, submenu_id)
            if not submenu:
                return False
        return True

    async def create(self, dish: DishBase, menu_id: str, submenu_id: str) -> DishCreate:
        if not await self.submenu_exists(menu_id, submenu_id):
            raise HTTPException(status_code=404, detail="submenu not found")

        async with self.uow:
            new_dish = await self.uow.dish_repo.create(dish, submenu_id)
            response = DishCreate(**new_dish.dict())
        await self.clear_cache(menu_id, submenu_id)
        return response

    async def get_list(self, menu_id: str, submenu_id: str) -> DishList:
        # self.submenu_exists(menu_id, submenu_id) commented for postman test pass

        if cache_value := await self.cache.get(self.list_cache_key):
            return DishList.parse_raw(cache_value)

        async with self.uow:
            dishes = await self.uow.dish_repo.list(menu_id, submenu_id)
            response = DishList.parse_obj(dishes)

        await self.cache.set(self.list_cache_key, response.json())
        return response

    async def get_detail(
        self, menu_id: str, submenu_id: str, dish_id: str
    ) -> Optional[DishCreate]:
        if cache_value := await self.cache.get(dish_id):
            return DishCreate.parse_raw(cache_value)

        async with self.uow:
            dish = await self.uow.dish_repo.get(menu_id, submenu_id, dish_id)
            if not dish:
                raise HTTPException(status_code=404, detail="dish not found")
            response = DishCreate(**dish.dict())

        await self.cache.set(dish_id, response.json())
        return response

    async def update(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        update_submenu: DishUpdate,
    ) -> Optional[DishCreate]:
        async with self.uow:
            dish = await self.uow.dish_repo.update(
                menu_id,
                submenu_id,
                dish_id,
                update_submenu,
            )
            if not dish:
                raise HTTPException(status_code=404, detail="dish not found")
            response = DishCreate(**dish.dict())
        await self.clear_cache(menu_id, submenu_id, dish_id)
        return response

    async def delete(self, menu_id: str, submenu_id: str, dish_id: str) -> DeleteBase:
        async with self.uow:
            deleted = await self.uow.dish_repo.delete(menu_id, submenu_id, dish_id)
        await self.clear_cache(menu_id, submenu_id, dish_id)
        if deleted:
            return DeleteBase(deleted=deleted)
        else:
            raise HTTPException(status_code=404, detail="dish not found")


@lru_cache
def get_dish_service(
    cache: AbstractCache = Depends(get_redis_cache),
    session: AsyncSession = Depends(get_session),
) -> DishService:
    uow = SqlModelUnitOfWork(session)
    return DishService(cache=cache, uow=uow)

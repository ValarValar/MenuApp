from functools import lru_cache
from typing import Optional

from fastapi import Depends, HTTPException
from pydantic.types import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.dishes import DishBase, DishDetail, DishList, DishUpdate
from api.v1.schemas.service import DeleteBase
from db.cache.base import AbstractCache
from db.cache.RedisCache import get_redis_cache
from db.db import get_session
from db.uow import SqlModelUnitOfWork
from services.base import ServiceBase


class DishService(ServiceBase):
    cache_list_key = "dish-list"
    cache_list_keys_to_clear = ["menu-list"]

    async def submenus_list_cache_key(self, menu_id: UUID) -> str:
        """
            As dish is related to one of submenus
        :param menu_id:
        :return:
        """
        return f"{str(menu_id)}_{self.cache_list_key}"

    async def dishes_list_cache_key(self, menu_id: UUID, submenu_id: UUID) -> str:
        return f"{str(menu_id)}_{str(submenu_id)}_{self.cache_list_key}"

    async def clear_cache(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: Optional[UUID] = None,
    ):
        keys_to_clear = [menu_id, submenu_id]
        if dish_id:
            keys_to_clear.append(dish_id)
        keys_to_clear.append(await self.submenus_list_cache_key(menu_id))
        keys_to_clear.append(await self.dishes_list_cache_key(menu_id, submenu_id))
        await self.cache.delete_list_keys(keys_to_clear)
        await self.cache.delete_list_keys(self.cache_list_keys_to_clear)

    async def submenu_exists(self, menu_id: UUID, submenu_id: UUID) -> bool:
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

    async def create(
        self, dish: DishBase, menu_id: UUID, submenu_id: UUID
    ) -> DishDetail:
        if not await self.submenu_exists(menu_id, submenu_id):
            raise HTTPException(status_code=404, detail="submenu not found")

        async with self.uow:
            new_dish = await self.uow.dish_repo.create(dish, submenu_id)
            response = DishDetail(**new_dish.dict())
        await self.clear_cache(menu_id, submenu_id)
        return response

    async def get_list(self, menu_id: UUID, submenu_id: UUID) -> DishList:
        # self.submenu_exists(menu_id, submenu_id) commented for postman test pass

        dishes_list_cache_key = await self.dishes_list_cache_key(menu_id, submenu_id)
        if cache_value := await self.cache.get(dishes_list_cache_key):
            return DishList.parse_raw(cache_value)

        async with self.uow:
            dishes = await self.uow.dish_repo.list(menu_id, submenu_id)
            response = DishList.parse_obj(dishes)

        await self.cache.set(dishes_list_cache_key, response.json())
        return response

    async def get_detail(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> Optional[DishDetail]:
        if cache_value := await self.cache.get(dish_id):
            return DishDetail.parse_raw(cache_value)

        async with self.uow:
            dish = await self.uow.dish_repo.get(menu_id, submenu_id, dish_id)
            if not dish:
                raise HTTPException(status_code=404, detail="dish not found")
            response = DishDetail(**dish.dict())

        await self.cache.set(dish_id, response.json())
        return response

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        update_submenu: DishUpdate,
    ) -> Optional[DishDetail]:
        async with self.uow:
            dish = await self.uow.dish_repo.update(
                menu_id,
                submenu_id,
                dish_id,
                update_submenu,
            )
            if not dish:
                raise HTTPException(status_code=404, detail="dish not found")
            response = DishDetail(**dish.dict())
        await self.clear_cache(menu_id, submenu_id, dish_id)
        return response

    async def delete(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> DeleteBase:
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

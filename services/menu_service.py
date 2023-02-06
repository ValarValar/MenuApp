from functools import lru_cache
from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.menus import MenuBase, MenuCreate, MenuDetail, MenuList, MenuUpdate
from api.v1.schemas.service import DeleteBase
from db.cache.base import AbstractCache
from db.cache.RedisCache import get_redis_cache
from db.db import get_session
from db.uow import SqlModelUnitOfWork
from services.mixin import ServiceBase


class MenuService(ServiceBase):
    list_cache_key = "menu-list"

    async def clear_cache(self, menu_id: str = ""):
        await self.cache.delete(menu_id)
        await self.cache.delete(self.list_cache_key)

    async def create(self, menu: MenuBase) -> MenuCreate:
        async with self.uow:
            new_menu = await self.uow.menu_repo.create(menu)
            response = MenuCreate(**new_menu.dict())
        await self.clear_cache()
        return response

    async def get_list(self) -> MenuList:
        if cache_value := await self.cache.get(self.list_cache_key):
            return MenuList.parse_raw(cache_value)

        async with self.uow:
            menus = await self.uow.menu_repo.list()
            response: MenuList = MenuList.parse_obj(menus)

        await self.cache.set(self.list_cache_key, response.json())
        return response

    async def get_detail(self, id: str) -> Optional[MenuDetail]:
        if cache_value := await self.cache.get(id):
            return MenuDetail.parse_raw(cache_value)

        async with self.uow:
            menu = await self.uow.menu_repo.get_detail(id)
            if not menu:
                raise HTTPException(status_code=404, detail="menu not found")
            response: MenuDetail = MenuDetail.parse_obj(menu)

        await self.cache.set(id, response.json())
        return response

    async def update(self, id: str, update_menu: MenuUpdate) -> MenuCreate:
        async with self.uow:
            updated_menu = await self.uow.menu_repo.update(id, update_menu)
            if not updated_menu:
                raise HTTPException(status_code=404, detail="menu not found")
            response = MenuCreate(**updated_menu.dict())
        await self.clear_cache(id)
        return response

    async def delete(self, id: str) -> DeleteBase:
        async with self.uow:
            deleted = await self.uow.menu_repo.delete(id)
        await self.clear_cache(id)
        if deleted:
            return DeleteBase(deleted=deleted)
        else:
            raise HTTPException(status_code=404, detail="menu not found")


@lru_cache
def get_menu_service(
    cache: AbstractCache = Depends(get_redis_cache),
    session: AsyncSession = Depends(get_session),
) -> MenuService:
    uow = SqlModelUnitOfWork(session)
    return MenuService(cache=cache, uow=uow)

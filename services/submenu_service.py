from functools import lru_cache
from typing import Optional

from fastapi import Depends, HTTPException
from pydantic.types import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.service import DeleteBase
from api.v1.schemas.submenus import (
    SubmenuBase,
    SubmenuCreate,
    SubmenuDetail,
    SubmenuList,
    SubmenuUpdate,
)
from db.cache.base import AbstractCache
from db.cache.RedisCache import get_redis_cache
from db.db import get_session
from db.uow import SqlModelUnitOfWork
from services.base import ServiceBase


class SubmenuService(ServiceBase):
    cache_list_key = "submenu-list"
    cache_list_keys_to_clear = ["menu-list"]

    async def submenus_list_cache_key(self, menu_id: UUID) -> str:
        """
            Returns cache key for submenus list in current menu
        :param menu_id:
        :return:
        """
        return f"{str(menu_id)}_{self.cache_list_key}"

    async def clear_cache(
        self,
        menu_id: UUID,
        submenu_id: Optional[UUID] = None,
    ):
        await self.cache.delete(menu_id)
        if submenu_id:
            await self.cache.delete(submenu_id)

        submenus_list_cache_key = await self.submenus_list_cache_key(menu_id)
        await self.cache.delete(submenus_list_cache_key)
        await self.cache.delete_list_keys(self.cache_list_keys_to_clear)

    async def menu_exists(self, menu_id: UUID) -> bool:
        """
        Checks that menu with menu_id exists,
        if not raises an exception
        :param menu_id:
        :return: None
        """
        async with self.uow:
            menu = await self.uow.menu_repo.get(menu_id)
            if not menu:
                return False
        return True

    async def create(self, submenu: SubmenuBase, menu_id: UUID) -> SubmenuCreate:
        if not await self.menu_exists(menu_id):
            raise HTTPException(status_code=404, detail="menu not found")

        async with self.uow:
            new_submenu = await self.uow.submenu_repo.create(submenu, menu_id)
            response = SubmenuCreate(**new_submenu.dict())
        await self.clear_cache(menu_id=menu_id)
        return response

    async def get_list(self, menu_id: UUID) -> SubmenuList:
        if not await self.menu_exists(menu_id):
            raise HTTPException(status_code=404, detail="menu not found")

        submenus_list_cache_key = await self.submenus_list_cache_key(menu_id)
        if cache_value := await self.cache.get(submenus_list_cache_key):
            return SubmenuList.parse_raw(cache_value)

        async with self.uow:
            submenus = await self.uow.submenu_repo.list(menu_id)
            response = SubmenuList.parse_obj(submenus)

        await self.cache.set(submenus_list_cache_key, response.json())
        return response

    async def get_detail(
        self, menu_id: UUID, submenu_id: UUID
    ) -> Optional[SubmenuDetail]:
        if cache_value := await self.cache.get(submenu_id):
            return SubmenuDetail.parse_raw(cache_value)

        async with self.uow:
            submenu = await self.uow.submenu_repo.get_detail(
                menu_id,
                submenu_id,
            )
            if not submenu:
                raise HTTPException(
                    status_code=404,
                    detail="submenu not found",
                )
            response = SubmenuDetail(**submenu)
        await self.cache.set(submenu_id, response.json())
        return response

    async def update(
        self, menu_id: UUID, submenu_id: UUID, update_submenu: SubmenuUpdate
    ) -> SubmenuCreate:
        async with self.uow:
            submenu = await self.uow.submenu_repo.update(
                menu_id,
                submenu_id,
                update_submenu,
            )
            if not submenu:
                raise HTTPException(
                    status_code=404,
                    detail="submenu not found",
                )
            response = SubmenuCreate(**submenu.dict())
        await self.clear_cache(menu_id=menu_id, submenu_id=submenu_id)
        return response

    async def delete(self, menu_id: UUID, submenu_id: UUID) -> DeleteBase:
        async with self.uow:
            deleted = await self.uow.submenu_repo.delete(menu_id, submenu_id)
        await self.clear_cache(menu_id=menu_id, submenu_id=submenu_id)
        if deleted:
            return DeleteBase(deleted=deleted)
        else:
            raise HTTPException(status_code=404, detail="menu not found")


@lru_cache
def get_submenu_service(
    cache: AbstractCache = Depends(get_redis_cache),
    session: AsyncSession = Depends(get_session),
) -> SubmenuService:
    uow = SqlModelUnitOfWork(session)
    return SubmenuService(cache=cache, uow=uow)

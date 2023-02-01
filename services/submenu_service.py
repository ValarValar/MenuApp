from functools import lru_cache
from typing import Optional

from fastapi import Depends, HTTPException
from sqlmodel import Session

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
from services.mixin import ServiceMixin


class SubmenuService(ServiceMixin):
    list_cache_key = 'submenu-list'

    def clear_cache(self, menu_id: str = '', submenu_id: str = ''):
        self.cache.delete(menu_id)
        self.cache.delete(submenu_id)
        self.cache.delete(self.list_cache_key)

    def menu_exists(self, menu_id: str) -> None:
        """
        Checks that menu with menu_id exists,
        if not raises an exception
        :param menu_id:
        :return: None
        """
        with self.uow:
            menu = self.uow.menu_repo.get_by_id(menu_id)
            if not menu:
                raise HTTPException(status_code=404, detail='menu not found')
        return

    def create(self, submenu: SubmenuBase, menu_id: str) -> SubmenuCreate:
        self.menu_exists(menu_id)
        with self.uow:
            new_submenu = self.uow.submenu_repo.create(submenu, menu_id)
            response = SubmenuCreate(**new_submenu.dict())
        self.clear_cache(menu_id)
        return response

    def get_list(self, menu_id: str) -> SubmenuList:
        self.menu_exists(menu_id)

        cache_value = self.cache.get(self.list_cache_key)
        if cache_value:
            return SubmenuList.parse_raw(cache_value)

        with self.uow:
            submenus = self.uow.submenu_repo.list(menu_id)
            response = SubmenuList.parse_obj(submenus)
        self.cache.set(self.list_cache_key, response.json())
        return response

    def get_detail(self, menu_id: str, submenu_id: str) -> Optional[SubmenuDetail]:
        cache_value = self.cache.get(submenu_id)
        if cache_value:
            return SubmenuDetail.parse_raw(cache_value)

        with self.uow:
            submenu = self.uow.submenu_repo.get_by_ids_with_count(
                menu_id, submenu_id,
            )
            if not submenu:
                raise HTTPException(
                    status_code=404, detail='submenu not found',
                )
            response = SubmenuDetail(**submenu)
        self.cache.set(submenu_id, response.json())
        return response

    def update(self, menu_id: str, submenu_id: str, update_submenu: SubmenuUpdate) -> SubmenuCreate:
        with self.uow:
            submenu = self.uow.submenu_repo.update(
                menu_id, submenu_id, update_submenu,
            )
            if not submenu:
                raise HTTPException(
                    status_code=404, detail='submenu not found',
                )
            response = SubmenuCreate(**submenu.dict())
        self.clear_cache(menu_id, submenu_id)
        return response

    def delete(self, menu_id: str, submenu_id: str) -> DeleteBase:
        with self.uow:
            deleted = self.uow.submenu_repo.delete(menu_id, submenu_id)
        self.clear_cache(menu_id, submenu_id)
        if deleted:
            return DeleteBase(deleted=deleted)
        else:
            raise HTTPException(status_code=404, detail='menu not found')


@lru_cache
def get_submenu_service(
        cache: AbstractCache = Depends(get_redis_cache),
        session: Session = Depends(get_session),
) -> SubmenuService:
    uow = SqlModelUnitOfWork(session)
    return SubmenuService(cache=cache, uow=uow)

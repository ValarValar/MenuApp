from functools import lru_cache
from typing import Optional

from fastapi import Depends, HTTPException
from sqlmodel import Session

from api.v1.schemas.menus import MenuBase, MenuCreate, MenuDetail, MenuList, MenuUpdate
from db.cache.base import AbstractCache
from db.cache.RedisCache import get_redis_cache
from db.db import get_session
from db.uow import SqlModelUnitOfWork
from services.mixin import ServiceMixin


class MenuService(ServiceMixin):
    list_cache_key = 'menu-list'

    def clear_cache(self, menu_id: str = ''):
        self.cache.delete(menu_id)
        self.cache.delete(self.list_cache_key)

    def create(self, menu: MenuBase) -> MenuCreate:
        with self.uow:
            new_menu = self.uow.menu_repo.create(menu)
            response = MenuCreate(**new_menu.dict())
        self.clear_cache()
        return response

    def get_list(self) -> MenuList:
        cache_value = self.cache.get(self.list_cache_key)
        if cache_value:
            return MenuList.parse_raw(cache_value)

        with self.uow:
            menus = self.uow.menu_repo.list()
            response: MenuList = MenuList.parse_obj(menus)

        self.cache.set(self.list_cache_key, response.json())
        return response

    def get_detail(self, id: str) -> Optional[MenuDetail]:
        cache_value = self.cache.get(id)
        if cache_value:
            return MenuDetail.parse_raw(cache_value)

        with self.uow:
            menu = self.uow.menu_repo.get_by_id_with_counts(id)
            if not menu:
                raise HTTPException(status_code=404, detail='menu not found')
            response: MenuDetail = MenuDetail.parse_obj(menu)

        self.cache.set(id, response.json())
        return response

    def update(self, id: str, update_menu: MenuUpdate) -> MenuCreate:
        with self.uow:
            updated_menu = self.uow.menu_repo.update(id, update_menu)
            if not updated_menu:
                raise HTTPException(status_code=404, detail='menu not found')
            response = MenuCreate(**updated_menu.dict())
        self.clear_cache(id)
        return response

    def delete(self, id: str) -> dict:
        with self.uow:
            deleted = self.uow.menu_repo.delete(id)
        self.clear_cache(id)
        if deleted:
            return {'deleted': deleted}
        else:
            raise HTTPException(status_code=404, detail='menu not found')


@lru_cache
def get_menu_service(
        cache: AbstractCache = Depends(get_redis_cache),
        session: Session = Depends(get_session),
) -> MenuService:
    uow = SqlModelUnitOfWork(session)
    return MenuService(cache=cache, uow=uow)

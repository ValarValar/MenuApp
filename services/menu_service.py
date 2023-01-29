from functools import lru_cache
from typing import Optional

from fastapi import Depends, HTTPException
from sqlmodel import Session

from api.v1.schemas.menus import MenuBase, MenuUpdate, MenuCreate, MenuDetail, MenuList
from db.cache.base import AbstractCache, get_cache
from db.db import get_session
from services.mixin import ServiceMixin
from db.uow import SqlModelUnitOfWork


class MenuService(ServiceMixin):
    def create(self, menu: MenuBase) -> MenuCreate:
        with self.uow:
            new_menu = self.uow.menu_repo.create(menu)
            response = MenuCreate(**new_menu.dict())
        return response

    def list(self) -> MenuList:
        with self.uow:
            menus = self.uow.menu_repo.list()
            response = MenuList.parse_obj(menus)
        return response

    def get(self, id: str) -> Optional[MenuDetail]:
        with self.uow:
            menu = self.uow.menu_repo.get_by_id_with_counts(id)
            if not menu:
                raise HTTPException(status_code=404, detail="menu not found")
            response = MenuDetail.parse_obj(menu)
        return response

    def update(self, id: str, update_menu: MenuUpdate) -> MenuCreate:
        with self.uow:
            updated_menu = self.uow.menu_repo.update(id, update_menu)
            if not updated_menu:
                raise HTTPException(status_code=404, detail="menu not found")
            response = MenuCreate(**updated_menu.dict())
        return response

    def delete(self, id: str) -> dict:
        with self.uow:
            deleted = self.uow.menu_repo.delete(id)
        if deleted:
            return {"deleted": deleted}
        else:
            raise HTTPException(status_code=404, detail="menu not found")


@lru_cache
def get_menu_service(
        cache: AbstractCache = Depends(get_cache),
        session: Session = Depends(get_session)
) -> MenuService:
    uow = SqlModelUnitOfWork(session)
    return MenuService(cache=cache, uow=uow)

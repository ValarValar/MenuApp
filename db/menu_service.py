from functools import lru_cache
from typing import Optional

from fastapi import Depends, HTTPException
from sqlmodel import Session

from api.v1.schemas.menus import MenuBase, MenuUpdate, MenuWithCount, MenuCreate, MenuDetail, MenuList
from db.cache.base import AbstractCache, get_cache
from db.db import get_session
from db.mixin import ServiceMixin
from db.uow import SqlModelUnitOfWork


class MenuService(ServiceMixin):
    def create(self, menu: MenuBase) -> MenuCreate:
        with self.uow:
            new_menu = self.uow.menu_repo.create(menu)
            response = MenuCreate(**new_menu.dict())
        return response

    def list(self) -> MenuList:
        with self.uow:
            results = self.uow.menu_repo.list()
            response = []
            for menu in results:
                submenus = menu.submenus
                submenus_count = len(submenus)
                dishes_count = sum([len(submenu.dishes) for submenu in submenus])
                response_model = MenuWithCount(
                    submenus_count=submenus_count,
                    dishes_count=dishes_count,
                    **menu.dict()
                )
                response.append(response_model)
        return response

    def get(self, id: str) -> Optional[MenuDetail]:
        with self.uow:
            results = self.uow.menu_repo.get_by_id_with_counts(id)
            if not results:
                raise HTTPException(status_code=404, detail="menu not found")
            submenus = results.submenus
            submenus_count = len(submenus)
            dishes_count = sum([len(submenu.dishes) for submenu in submenus])
            response = MenuWithCount(
                submenus_count=submenus_count,
                dishes_count=dishes_count,
                **results.dict()
            )
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

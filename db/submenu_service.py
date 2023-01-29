from functools import lru_cache
from typing import Optional

from fastapi import Depends, HTTPException
from sqlmodel import Session

from api.v1.schemas.submenus import (
    SubmenuBase,
    SubmenuUpdate,
    SubmenuCreate,
    SubmenuList,
    SubmenuDetail
)
from db.cache.base import AbstractCache, get_cache
from db.db import get_session
from db.mixin import ServiceMixin
from db.uow import SqlModelUnitOfWork


class SubmenuService(ServiceMixin):
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
                raise HTTPException(status_code=404, detail="menu not found")
        return

    def create(self, submenu: SubmenuBase, menu_id: str) -> SubmenuCreate:
        self.menu_exists(menu_id)
        with self.uow:
            new_submenu = self.uow.submenu_repo.create(submenu, menu_id)
            response = SubmenuCreate(**new_submenu)
        return response

    def list(self, menu_id: str) -> list[SubmenuList]:
        self.menu_exists(menu_id)
        with self.uow:
            submenus = self.uow.submenu_repo.list(menu_id)
            response = SubmenuList.parse_obj(submenus)

        return response

    def get(self, menu_id: str, submenu_id: str) -> Optional[SubmenuDetail]:
        with self.uow:
            submenu = self.uow.submenu_repo.get_by_ids_with_count(menu_id, submenu_id)
            if not submenu:
                raise HTTPException(status_code=404, detail="submenu not found")
            response = SubmenuDetail(**submenu)
        return response

    def update(self, menu_id: str, submenu_id: str, update_submenu: SubmenuUpdate) -> SubmenuCreate:
        with self.uow:
            submenu = self.uow.submenu_repo.update(menu_id, submenu_id, update_submenu)
            if not submenu:
                raise HTTPException(status_code=404, detail="submenu not found")
            response = SubmenuCreate(**submenu)
        return response

    def delete(self, menu_id: str, submenu_id: str) -> dict:
        with self.uow:
            deleted = self.uow.submenu_repo.delete(menu_id, submenu_id)
        if deleted:
            return {"deleted": deleted}
        else:
            raise HTTPException(status_code=404, detail="menu not found")


@lru_cache
def get_submenu_service(
        cache: AbstractCache = Depends(get_cache),
        session: Session = Depends(get_session)
) -> SubmenuService:
    uow = SqlModelUnitOfWork(session)
    return SubmenuService(cache=cache, uow=uow)

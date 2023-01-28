from functools import lru_cache
from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from api.v1.schemas.submenus import SubmenuBase, SubmenuUpdate, SubmenuCreate, SubmenuWithCount
from db.cache.base import AbstractCache, get_cache
from db.db import get_session
from db.menu_db_service import MenuDbService
from db.mixin import ServiceMixin
from db.uow import SqlModelUnitOfWork
from models import Submenu


class SubmenuDbService(ServiceMixin):
    @staticmethod
    def menu_exists(menu_id: str) -> None:
        """
        Checks that menu with menu_id exists,
        if not raises an exception
        :param menu_id:
        :return: None
        """
        # menu = menu_db.get_menu_by_id(menu_id)
        # if not menu:
        #    raise HTTPException(status_code=404, detail="menu not found")


    def create_submenu(self, submenu: SubmenuBase, menu_id: str) -> SubmenuCreate:
        self.menu_exists(menu_id)

        new_submenu = Submenu(menu_id=menu_id, **submenu.dict())
        self.session.add(new_submenu)
        self.session.commit()
        self.session.refresh(new_submenu)

        return SubmenuCreate(**new_submenu.dict())

    def list_submenus(self, menu_id: str) -> list[SubmenuWithCount]:
        self.menu_exists(menu_id)

        statement = select(Submenu).where(Submenu.menu_id == menu_id).options(joinedload(Submenu.dishes))
        results = self.session.exec(statement).unique().all()

        response = []
        for submenu in results:
            dishes_count = len(submenu.dishes)
            response.append(SubmenuWithCount(dishes_count=dishes_count, **submenu.dict()))
        return response

    def get_submenu_by_ids(self, menu_id: str, submenu_id: str) -> Optional[SubmenuWithCount]:
        statement = select(Submenu).where(Submenu.menu_id == menu_id).where(Submenu.id == submenu_id)
        detailed_submenu = self.session.exec(statement).first()

        if not detailed_submenu:
            raise HTTPException(status_code=404, detail="submenu not found")
        dishes_count = len(detailed_submenu.dishes)
        return SubmenuWithCount(dishes_count=dishes_count, **detailed_submenu.dict())

    def get_submenu_by_ids_with_count(self, menu_id: str, submenu_id: str) -> Optional[Submenu]:
        statement = select(Submenu) \
            .where(Submenu.menu_id == menu_id) \
            .where(Submenu.id == submenu_id) \
            .options(joinedload(Submenu.dishes))
        submenu = self.session.exec(statement).first()
        return submenu

    def update_submenu(self, menu_id: str, submenu_id: str, update_submenu: SubmenuUpdate) -> Optional[SubmenuCreate]:
        submenu = self.get_submenu_by_ids(menu_id, submenu_id)
        if submenu:
            update_menu = update_submenu.dict(exclude_unset=True)
            for key, value in update_menu.items():
                setattr(submenu, key, value)
            self.session.add(submenu)
            self.session.commit()
            self.session.refresh(submenu)

        if not submenu:
            raise HTTPException(status_code=404, detail="submenu not found")

        return SubmenuCreate(**submenu.dict())

    def delete_submenu(self, menu_id: str, submenu_id: str) -> dict:
        current_submenu = self.get_submenu_by_ids(menu_id, submenu_id)
        if current_submenu:
            self.session.delete(current_submenu)
            self.session.commit()
            return {"deleted": True}
        raise HTTPException(status_code=404, detail="submenu not found")


@lru_cache
def get_submenu_db_service(
        cache: AbstractCache = Depends(get_cache),
        session: Session = Depends(get_session)
) -> MenuDbService:
    uow = SqlModelUnitOfWork(session)
    return MenuDbService(cache=cache, uow=uow)

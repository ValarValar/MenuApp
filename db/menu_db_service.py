from functools import lru_cache
from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from api.v1.schemas.menus import MenuBase, MenuUpdate, MenuWithCount, MenuCreate
from db.cache.base import AbstractCache, get_cache
from db.db import get_session
from db.mixin import ServiceMixin
from db.uow import SqlModelUnitOfWork
from models import Submenu
from models.menu import Menu


class MenuDbService(ServiceMixin):
    def create_menu(self, menu: MenuBase) -> MenuCreate:
        new_menu = Menu(title=menu.title, description=menu.description)
        self.session.add(new_menu)
        self.session.commit()
        self.session.refresh(new_menu)
        return MenuCreate(**new_menu.dict())

    def list_menu(self) -> list[MenuWithCount]:
        results = self.session.exec(
            select(Menu).options(joinedload(Menu.submenus).joinedload(Submenu.dishes))).unique().all()
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

    def get_menu_by_id(self, id: str) -> Optional[Menu]:
        menu = self.session.get(Menu, id)
        return menu

    def get_menu_by_id_with_counts(self, id: str) -> Optional[MenuWithCount]:
        statement = select(Menu) \
            .where(Menu.id == id) \
            .options(joinedload(Menu.submenus).joinedload(Submenu.dishes))
        results = self.session.exec(statement).first()
        if not results:
            raise HTTPException(status_code=404, detail="menu not found")

        submenus = results.submenus
        submenus_count = len(submenus)
        dishes_count = sum([len(submenu.dishes) for submenu in submenus])
        response_model = MenuWithCount(
            submenus_count=submenus_count,
            dishes_count=dishes_count,
            **results.dict()
        )
        return response_model

    def update_menu(self, id: str, update_menu: MenuUpdate) -> MenuCreate:
        current_menu = self.get_menu_by_id(id)
        if current_menu:
            update_menu = update_menu.dict(exclude_unset=True)
            for key, value in update_menu.items():
                setattr(current_menu, key, value)
            self.session.add(current_menu)
            self.session.commit()
            self.session.refresh(current_menu)

        if not current_menu:
            raise HTTPException(status_code=404, detail="menu not found")

        return MenuCreate(**current_menu.dict())

    def delete_menu(self, id: str) -> dict:
        current_menu = self.get_menu_by_id(id)
        if current_menu:
            self.session.delete(current_menu)
            self.session.commit()
            return {"deleted": True}
        raise HTTPException(status_code=404, detail="menu not found")


@lru_cache
def get_menu_db_service(
        cache: AbstractCache = Depends(get_cache),
        session: Session = Depends(get_session)
) -> MenuDbService:
    uow = SqlModelUnitOfWork(session)
    return MenuDbService(cache=cache, uow=uow)

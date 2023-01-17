from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlalchemy import func
from sqlmodel import Session, select

from api.v1.schemas.menus import MenuBase, MenuUpdate
from db.db import get_session
from db.mixin import ServiceMixin
from models import Submenu, Dish
from models.menu import Menu


class MenuDbService(ServiceMixin):
    def create_menu(self, menu: MenuBase) -> Menu:
        new_menu = Menu(title=menu.title, description=menu.description)
        self.session.add(new_menu)
        self.session.commit()
        self.session.refresh(new_menu)
        return new_menu

    def list_menu(self) -> list[Menu]:
        results = self.session.exec(select(Menu)).all()
        for item in results:
            print(item)
        return results

    def get_menu_by_id(self, id: str) -> Optional[Menu]:
        menu = self.session.get(Menu, id)
        return menu

    def get_menu_by_id_with_counts(self, id: str):
        """
        not finished
        :param id:
        :return:
        """
        statement = select(Menu).where(Menu.id == id).join(Menu, Submenu).join(Dish)
        results = self.session.exec(statement).all()
        dishes_count = len(results)

        statement = select(Menu).\
            where(Menu.id == id).\
            select(Menu.id, func.count(Menu.submenus)).group_by(Menu.id)


    def update_menu(self, id: str, update_menu: MenuUpdate) -> Optional[Menu]:
        current_menu = self.get_menu_by_id(id)
        if current_menu:
            update_menu = update_menu.dict(exclude_unset=True)
            for key, value in update_menu.items():
                setattr(current_menu, key, value)
            self.session.add(current_menu)
            self.session.commit()
            self.session.refresh(current_menu)
        return current_menu

    def delete_menu(self, id: str) -> bool:
        current_menu = self.get_menu_by_id(id)
        if current_menu:
            self.session.delete(current_menu)
            self.session.commit()
            return True
        return False


@lru_cache
def get_menu_db_service(session: Session = Depends(get_session)) -> MenuDbService:
    return MenuDbService(session)

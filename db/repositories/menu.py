from typing import Optional

from sqlalchemy.orm import joinedload
from sqlmodel import select

from api.v1.schemas.menus import MenuBase, MenuUpdate
from db.repositories.base import AbstractRepository
from models import Menu


class MenuRepository(AbstractRepository):

    def add(self, menu: MenuBase) -> Menu:
        new_menu = Menu.from_orm(menu)
        self.session.add(new_menu)
        return new_menu

    def list(self) -> list[Menu]:
        results = self.session.exec(
            select(Menu).options(joinedload("Menu.submenus").joinedload("Submenu.dishes"))).unique().all()
        return results

    def get_by_id(self, id: str) -> Optional[Menu]:
        menu = self.session.get(Menu, id)
        return menu

    def get_by_id_with_counts(self, id: str) -> Optional[Menu]:
        statement = select(Menu) \
            .where(Menu.id == id) \
            .options(joinedload("Menu.submenus").joinedload("Submenu.dishes"))
        results = self.session.exec(statement).first()
        return results

    def update(self, id: str, update_menu: MenuUpdate) -> Menu:
        menu = self.get_by_id(id)
        if menu:
            update_menu = update_menu.dict(exclude_unset=True)
            for key, value in update_menu.items():
                setattr(menu, key, value)
            self.session.add(menu)
            self.session.commit()
            self.session.refresh(menu)
        return menu

    def delete(self, id: str) -> bool:
        menu = self.get_by_id(id)
        if menu:
            self.session.delete(menu)
            self.session.commit()
            return True
        return False


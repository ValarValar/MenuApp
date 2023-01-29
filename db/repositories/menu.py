from typing import Optional

from sqlalchemy import func, text, select, Integer
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import coalesce

from api.v1.schemas.menus import MenuBase, MenuUpdate
from db.repositories.base import AbstractRepository
from models import Menu, Submenu


class MenuRepository(AbstractRepository):
    def create(self, menu: MenuBase) -> Menu:
        new_menu = Menu.from_orm(menu)
        self.session.add(new_menu)
        return new_menu

    def list(self) -> list[Menu]:
        subquery = select(
            Submenu.id,
            Submenu.description,
            Submenu.title,
            Submenu.menu_id,
            func.count(Submenu.dishes).label("dishes_count")
        ).join(
            Submenu.dishes, isouter=True
        ).group_by(Submenu.id).subquery()
        statement = select(
            Menu.id,
            Menu.description,
            Menu.title,
            func.count(subquery.c.id).label("submenus_count"),
            func.coalesce(func.sum(subquery.c.dishes_count), 0).label("dishes_count")
        ).outerjoin(
            subquery, Menu.id == subquery.c.menu_id
        ).group_by(Menu.id)
        results = self.session.exec(statement).all()
        return results

    def get_by_id(self, id: str) -> Optional[Menu]:
        menu = self.session.get(Menu, id)
        return menu

    def get_by_id_with_counts(self, id: str) -> Optional[Menu]:
        subquery = select(
            Submenu.id,
            Submenu.description,
            Submenu.title,
            Submenu.menu_id,
            func.count(Submenu.dishes).label("dishes_count")
        ).where(
            Submenu.menu_id == id
        ).join(
            Submenu.dishes, isouter=True
        ).group_by(Submenu.id).subquery()
        statement = select(
            Menu.id,
            Menu.description,
            Menu.title,
            func.count(subquery.c.id).label("submenus_count"),
            func.coalesce(func.sum(subquery.c.dishes_count), 0).label("dishes_count")
        ).where(
            Menu.id == id
        ).outerjoin(
            subquery, Menu.id == subquery.c.menu_id
        ).group_by(Menu.id)
        results = self.session.exec(statement).one_or_none()
        return results

    def update(self, id: str, update_menu: MenuUpdate) -> Menu:
        menu = self.get_by_id(id)
        if menu:
            update_menu = update_menu.dict(exclude_unset=True)
            for key, value in update_menu.items():
                setattr(menu, key, value)
            self.session.add(menu)
        return menu

    def delete(self, id: str) -> bool:
        menu = self.get_by_id(id)
        if menu:
            self.session.delete(menu)
            return True
        return False

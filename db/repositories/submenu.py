from typing import Optional

from sqlalchemy import func
from sqlmodel import select

from api.v1.schemas.submenus import SubmenuBase, SubmenuUpdate
from db.repositories.base import AbstractRepository
from models import Submenu, Dish


class SubmenuRepository(AbstractRepository):

    def create(self, submenu: SubmenuBase, menu_id: str) -> Submenu:
        new_submenu = Submenu(menu_id=menu_id, **submenu.dict())
        self.session.add(new_submenu)
        return new_submenu

    def list(self, menu_id: str) -> list[Submenu]:
        statement = select(
            Submenu.id,
            Submenu.description,
            Submenu.title,
            func.count(Submenu.dishes).label("dishes_count")
        ).where(
            Submenu.menu_id == menu_id
        ).join(
            Submenu.dishes, isouter=True
        ).group_by(Submenu.id)
        results = self.session.execute(statement=statement).all()
        return results

    def get_by_ids(self, menu_id: str, submenu_id: str) -> Optional[Submenu]:
        statement = select(Submenu).where(Submenu.menu_id == menu_id).where(Submenu.id == submenu_id)
        detailed_submenu = self.session.exec(statement).one_or_none()
        return detailed_submenu

    def get_by_ids_with_count(self, menu_id: str, submenu_id: str) -> Optional[Submenu]:
        statement = select(
            Submenu.id,
            Submenu.description,
            Submenu.title,
            func.count(Submenu.dishes).label("dishes_count")
        ).where(
            Submenu.menu_id == menu_id
        ).where(
            Submenu.id == submenu_id
        ).join(Submenu.dishes, isouter=True).group_by(Submenu.id)
        submenu = self.session.exec(statement).one_or_none()
        return submenu

    def update(self, menu_id: str, submenu_id: str, update_submenu: SubmenuUpdate) -> Submenu:
        submenu = self.get_by_ids(menu_id, submenu_id)
        if submenu:
            update_menu = update_submenu.dict(exclude_unset=True)
            for key, value in update_menu.items():
                setattr(submenu, key, value)
            self.session.add(submenu)
        return submenu

    def delete(self, menu_id: str, submenu_id: str) -> bool:
        current_submenu = self.get_by_ids(menu_id, submenu_id)
        if current_submenu:
            self.session.delete(current_submenu)
            return True
        return False
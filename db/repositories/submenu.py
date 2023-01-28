from typing import Optional

from sqlalchemy.orm import joinedload
from sqlmodel import select

from api.v1.schemas.submenus import SubmenuBase, SubmenuUpdate
from db.repositories.base import AbstractRepository
from models import Submenu


class SubmenuRepository(AbstractRepository):

    def create(self, submenu: SubmenuBase, menu_id: str) -> Submenu:
        new_submenu = Submenu(menu_id=menu_id, **submenu.dict())
        self.session.add(new_submenu)
        return new_submenu

    def list(self, menu_id: str) -> list[Submenu]:
        statement = select(Submenu).where(Submenu.menu_id == menu_id).options(joinedload(Submenu.dishes))
        results = self.session.exec(statement).unique().all()
        return results

    def get_by_ids(self, menu_id: str, submenu_id: str) -> Optional[Submenu]:
        statement = select(Submenu).where(Submenu.menu_id == menu_id).where(Submenu.id == submenu_id)
        detailed_submenu = self.session.exec(statement).first()
        return detailed_submenu

    def get_by_ids_with_count(self, menu_id: str, submenu_id: str):
        statement = select(Submenu) \
            .where(Submenu.menu_id == menu_id) \
            .where(Submenu.id == submenu_id) \
            .options(joinedload(Submenu.dishes))
        submenu = self.session.exec(statement).first()

    def update(self, menu_id: str, submenu_id: str, update_submenu: SubmenuUpdate):
        submenu = self.get_by_ids(menu_id, submenu_id)
        if submenu:
            update_menu = update_submenu.dict(exclude_unset=True)
            for key, value in update_menu.items():
                setattr(submenu, key, value)
            self.session.add(submenu)

    def delete(self, menu_id: str, submenu_id: str) -> bool:
        current_submenu = self.get_by_ids(menu_id, submenu_id)
        if current_submenu:
            self.session.delete(current_submenu)
            return True
        return False
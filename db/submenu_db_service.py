from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from api.v1.schemas.submenus import SubmenuBase, SubmenuUpdate
from db.db import get_session
from db.mixin import ServiceMixin
from models import Submenu


class SubmenuDbService(ServiceMixin):
    def create_submenu(self, submenu: SubmenuBase, menu_id: str) -> Submenu:
        new_submenu = Submenu(menu_id=menu_id, **submenu.dict())
        self.session.add(new_submenu)
        self.session.commit()
        self.session.refresh(new_submenu)
        return new_submenu

    def list_submenus(self, menu_id: str) -> list[Submenu]:
        statement = select(Submenu).where(Submenu.menu_id == menu_id).options(joinedload(Submenu.dishes))
        results = self.session.exec(statement).unique().all()
        return results

    def get_submenu_by_ids(self, menu_id: str, submenu_id: str) -> Optional[Submenu]:
        statement = select(Submenu).where(Submenu.menu_id == menu_id).where(Submenu.id == submenu_id)
        submenu = self.session.exec(statement).first()
        return submenu

    def get_submenu_by_ids_with_count(self, menu_id: str, submenu_id: str) -> Optional[Submenu]:
        statement = select(Submenu) \
            .where(Submenu.menu_id == menu_id) \
            .where(Submenu.id == submenu_id) \
            .options(joinedload(Submenu.dishes))
        submenu = self.session.exec(statement).first()
        return submenu

    def update_submenu(self, menu_id: str, submenu_id: str, update_submenu: SubmenuUpdate) -> Optional[Submenu]:
        current_submenu = self.get_submenu_by_ids(menu_id, submenu_id)
        if current_submenu:
            update_menu = update_submenu.dict(exclude_unset=True)
            for key, value in update_menu.items():
                setattr(current_submenu, key, value)
            self.session.add(current_submenu)
            self.session.commit()
            self.session.refresh(current_submenu)
        return current_submenu

    def delete_submenu(self, menu_id: str, submenu_id: str) -> bool:
        current_submenu = self.get_submenu_by_ids(menu_id, submenu_id)
        if current_submenu:
            self.session.delete(current_submenu)
            self.session.commit()
            return True
        return False


@lru_cache
def get_submenu_db_service(session: Session = Depends(get_session)) -> SubmenuDbService:
    return SubmenuDbService(session)

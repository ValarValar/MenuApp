from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlmodel import Session

from api.v1.schemas.menus import MenuBase, MenuUpdate
from db.db import get_session
from db.mixin_db_service import CRUDDBServiceMixin
from models.menu import Menu


class MenuDbService(CRUDDBServiceMixin):
    def __init__(self, session: Session):
        super().__init__(session, Menu)

    def create_item(self, menu: MenuBase) -> Menu:
        return super().create_item(menu)

    def list_items(self) -> list[Menu]:
        return super().list_items()

    def get_item_by_id(self, id: str) -> Optional[Menu]:
        return super().get_item_by_id(id)

    def update_item(self, id: str, update_menu: MenuUpdate) -> Optional[Menu]:
        return super().update_item(id, update_menu)

    def delete_item(self, id: str) -> bool:
        return super().delete_item(id)


@lru_cache
def get_menu_db_service(session: Session = Depends(get_session)) -> MenuDbService:
    return MenuDbService(session)

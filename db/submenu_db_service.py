from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlmodel import Session

from api.v1.schemas.submenus import SubmenuBase, SubmenuUpdate
from db.db import get_session
from db.mixin_db_service import CRUDDBServiceMixin
from models import Submenu


class SubmenuDbService(CRUDDBServiceMixin):
    def __init__(self, session: Session):
        super().__init__(session, Submenu)

    def create_item(self, menu: SubmenuBase) -> Submenu:
        return super().create_item(menu)

    def list_items(self) -> list[Submenu]:
        return super().list_items()

    def get_item_by_id(self, id: str) -> Optional[Submenu]:
        return super().get_item_by_id(id)

    def update_item(self, id: str, update_submenu: SubmenuUpdate) -> Optional[Submenu]:
        return super().update_item(id, update_submenu)

    def delete_item(self, id: str) -> bool:
        return super().delete_item(id)


@lru_cache
def get_submenu_db_service(session: Session = Depends(get_session)) -> SubmenuDbService:
    return SubmenuDbService(session)

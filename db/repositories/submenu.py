from typing import Optional

from pydantic.types import UUID
from sqlalchemy import func, select

from api.v1.schemas.submenus import SubmenuBase, SubmenuUpdate
from db.repositories.base import AbstractRepository
from models import Submenu


class SubmenuRepository(AbstractRepository):
    async def create(self, submenu: SubmenuBase, menu_id: UUID) -> Submenu:
        new_submenu = Submenu(menu_id=menu_id, **submenu.dict())
        self.session.add(new_submenu)
        return new_submenu

    async def list(self, menu_id: UUID) -> list[Submenu]:
        statement = (
            select(
                Submenu.id,
                Submenu.description,
                Submenu.title,
                func.count(Submenu.dishes).label("dishes_count"),
            )
            .where(
                Submenu.menu_id == menu_id,
            )
            .join(
                Submenu.dishes,
                isouter=True,
            )
            .group_by(Submenu.id)
        )
        results = await self.session.execute(statement=statement)
        submenus: list[Submenu] = results.all()
        return submenus

    async def get(self, menu_id: UUID, submenu_id: UUID) -> Optional[Submenu]:
        statement = (
            select(Submenu)
            .where(
                Submenu.menu_id == menu_id,
            )
            .where(Submenu.id == submenu_id)
        )
        results = await self.session.execute(statement)
        detailed_submenu: Optional[Submenu] = results.scalar_one_or_none()
        return detailed_submenu

    async def get_detail(self, menu_id: UUID, submenu_id: UUID) -> Optional[Submenu]:
        statement = (
            select(
                Submenu.id,
                Submenu.description,
                Submenu.title,
                func.count(Submenu.dishes).label("dishes_count"),
            )
            .where(
                Submenu.menu_id == menu_id,
            )
            .where(
                Submenu.id == submenu_id,
            )
            .join(Submenu.dishes, isouter=True)
            .group_by(Submenu.id)
        )
        results = await self.session.execute(statement)
        submenu: Optional[Submenu] = results.one_or_none()
        return submenu

    async def update(
        self, menu_id: UUID, submenu_id: UUID, update_submenu: SubmenuUpdate
    ) -> Optional[Submenu]:
        if submenu := await self.get(menu_id, submenu_id):
            update_menu = update_submenu.dict(exclude_unset=True)
            for key, value in update_menu.items():
                setattr(submenu, key, value)
            self.session.add(submenu)
        return submenu

    async def delete(self, menu_id: UUID, submenu_id: UUID) -> bool:
        if current_submenu := await self.get(menu_id, submenu_id):
            await self.session.delete(current_submenu)
            return True
        return False

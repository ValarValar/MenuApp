from typing import Optional

from pydantic.types import UUID
from sqlalchemy import func, select

from api.v1.schemas.menus import MenuBase, MenuUpdate
from db.repositories.base import AbstractRepository
from models import Menu, Submenu


class MenuRepository(AbstractRepository):
    async def create(self, menu: MenuBase) -> Menu:
        new_menu = Menu.from_orm(menu)
        self.session.add(new_menu)
        return new_menu

    async def list(self) -> list[Menu]:
        subquery = (
            select(
                Submenu.id,
                Submenu.description,
                Submenu.title,
                Submenu.menu_id,
                func.count(Submenu.dishes).label("dishes_count"),
            )
            .join(
                Submenu.dishes,
                isouter=True,
            )
            .group_by(Submenu.id)
            .subquery()
        )
        statement = (
            select(
                Menu.id,
                Menu.description,
                Menu.title,
                func.count(subquery.c.id).label("submenus_count"),
                func.coalesce(
                    func.sum(subquery.c.dishes_count),
                    0,
                ).label("dishes_count"),
            )
            .outerjoin(
                subquery,
                Menu.id == subquery.c.menu_id,
            )
            .group_by(Menu.id)
        )
        results = await self.session.execute(statement)
        menus: list[Menu] = results.all()
        return menus

    async def get(self, id: UUID) -> Optional[Menu]:
        menu = await self.session.get(Menu, id)
        return menu

    async def get_detail(self, id: UUID) -> Optional[Menu]:
        subquery = (
            select(
                Submenu.id,
                Submenu.description,
                Submenu.title,
                Submenu.menu_id,
                func.count(Submenu.dishes).label("dishes_count"),
            )
            .where(
                Submenu.menu_id == id,
            )
            .join(
                Submenu.dishes,
                isouter=True,
            )
            .group_by(Submenu.id)
            .subquery()
        )
        statement = (
            select(
                Menu.id,
                Menu.description,
                Menu.title,
                func.count(subquery.c.id).label("submenus_count"),
                func.coalesce(
                    func.sum(subquery.c.dishes_count),
                    0,
                ).label("dishes_count"),
            )
            .where(
                Menu.id == id,
            )
            .outerjoin(
                subquery,
                Menu.id == subquery.c.menu_id,
            )
            .group_by(Menu.id)
        )
        results = await self.session.execute(statement)
        menu: Optional[Menu] = results.one_or_none()
        return menu

    async def update(self, id: UUID, update_menu: MenuUpdate) -> Optional[Menu]:
        if menu := await self.get(id):
            update_menu = update_menu.dict(exclude_unset=True)
            for key, value in update_menu.items():
                setattr(menu, key, value)
            self.session.add(menu)
        return menu

    async def delete(self, id: UUID) -> bool:
        if menu := await self.get(id):
            await self.session.delete(menu)
            return True
        return False

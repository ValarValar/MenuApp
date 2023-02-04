from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.dishes import DishBase
from api.v1.schemas.menus import MenuBase
from api.v1.schemas.service import TestDataBase
from api.v1.schemas.submenus import SubmenuBase
from db.cache.base import AbstractCache, get_cache
from db.db import get_session
from db.test_data import TEST_DATA
from db.uow import SqlModelUnitOfWork
from services.mixin import ServiceMixin


class DataService(ServiceMixin):
    async def fill_db_with_test_data(self) -> TestDataBase:
        for menu in TEST_DATA:
            async with self.uow:
                new_menu = await self.uow.menu_repo.create(MenuBase(**menu['menu']))
                menu_id = new_menu.id

            for submenu in menu['submenus']:
                async with self.uow:
                    new_submenu = await self.uow.submenu_repo.create(
                        submenu=SubmenuBase(menu_id=menu_id, **submenu['submenu']),
                        menu_id=menu_id,
                    )
                    submenu_id = new_submenu.id

                for dish in submenu['dishes']:
                    async with self.uow:
                        new_dish = await self.uow.dish_repo.create(
                            dish=DishBase(submenu_id=submenu_id, **dish),
                            submenu_id=submenu_id
                        )
        return TestDataBase(push_test_data=True)


@lru_cache
def get_data_service(
        cache: AbstractCache = Depends(get_cache),
        session: AsyncSession = Depends(get_session),
) -> DataService:
    uow = SqlModelUnitOfWork(session)
    return DataService(cache=cache, uow=uow)

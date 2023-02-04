from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories.dish import DishRepository
from db.repositories.menu import MenuRepository
from db.repositories.submenu import SubmenuRepository


class SqlModelUnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.menu_repo = MenuRepository(session=session)
        self.submenu_repo = SubmenuRepository(session=session)
        self.dish_repo = DishRepository(session=session)

    async def __aenter__(self, *args):
        return self

    async def __aexit__(self, *args):
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
        finally:
            await self.session.close()

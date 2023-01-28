from sqlmodel import Session

from db.repositories.dish import DishRepository
from db.repositories.menu import MenuRepository
from db.repositories.submenu import SubmenuRepository


class SqlModelUnitOfWork:
    def __init__(self, session: Session):
        self.session = session
        self.menu_repo = MenuRepository(session=session)
        self.submenu_repo = SubmenuRepository(session=session)
        self.dish_repo = DishRepository(session=session)

    def __enter__(self, *args):
        return self

    def __exit__(self):
        try:
            self.session.commit()
        except:
            self.session.rollback()
        finally:
            self.session.close()

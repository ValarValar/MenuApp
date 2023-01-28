from db.repositories.base import AbstractRepository
from models import Submenu


class SubmenuRepository(AbstractRepository):
    model:type[Submenu] = Submenu

from db.repositories.base import AbstractRepository
from models import Dish


class DishRepository(AbstractRepository):
    model: type[Dish] = Dish

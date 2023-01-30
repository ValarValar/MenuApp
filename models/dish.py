import uuid as uuid_pkg

from pydantic import condecimal
from sqlmodel import Field, Relationship

from models.submenu import Submenu
from models.uuid import UUIDModel


class Dish(UUIDModel, table=True):
    title: str
    description: str
    price: condecimal(decimal_places=2) = Field(default=0)
    submenu_id: uuid_pkg.UUID = Field(foreign_key='submenu.id')
    submenu: Submenu = Relationship(back_populates='dishes')

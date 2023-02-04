import uuid as uuid_pkg
from typing import Optional

from sqlmodel import Field, Relationship

from models.menu import Menu
from models.uuid import UUIDModel


class Submenu(UUIDModel, table=True):
    title: str
    description: str
    menu_id: uuid_pkg.UUID = Field(foreign_key="menu.id")
    menu: Menu = Relationship(back_populates="submenus")
    dishes: Optional[list["Dish"]] = Relationship(
        back_populates="submenu",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

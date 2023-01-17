from typing import Optional, List

from sqlmodel import Relationship

from models.uuid import UUIDModel


class Menu(UUIDModel, table=True):
    title: str
    description: str
    submenus: Optional[List["Submenu"]] = Relationship(back_populates="menu")

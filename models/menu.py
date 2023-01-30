from typing import Optional

from sqlmodel import Relationship

from models.uuid import UUIDModel


class Menu(UUIDModel, table=True):
    title: str
    description: str
    submenus: Optional[list['Submenu']] = Relationship(
        back_populates='menu',
        sa_relationship_kwargs={'cascade': 'all, delete-orphan'},
    )

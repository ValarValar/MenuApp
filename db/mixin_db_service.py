from abc import abstractmethod, ABC
from typing import Optional, Type

from pydantic.main import BaseModel
from sqlmodel import Session, SQLModel, select


class CRUDDBServiceMixin(ABC):

    def __init__(self, session: Session, model: Type[SQLModel]):
        self.session: Session = session
        self.model_type: Type[SQLModel] = model

    @abstractmethod
    def create_item(self, item_base: BaseModel) -> SQLModel:
        new_item = self.model_type(**item_base.dict())
        self.session.add(new_item)
        self.session.commit()
        self.session.refresh(new_item)
        return new_item

    @abstractmethod
    def list_items(self) -> list[SQLModel]:
        results = self.session.exec(select(self.model_type)).all()
        return results

    @abstractmethod
    def get_item_by_id(self, id: str) -> Optional[SQLModel]:
        user = self.session.get(self.model_type, id)
        return user

    @abstractmethod
    def update_item(self, id: str, update_item: BaseModel) -> Optional[SQLModel]:
        current_item = self.get_item_by_id(id)
        update_item = update_item.dict(exclude_unset=True)
        if current_item:
            for key, value in update_item.items():
                setattr(current_item, key, value)
            self.session.add(current_item)
            self.session.commit()
            self.session.refresh(current_item)
        return current_item

    @abstractmethod
    def delete_item(self, id: str) -> bool:
        current_item = self.get_item_by_id(id)
        if current_item:
            self.session.delete(current_item)
            self.session.commit()
            return True
        return False

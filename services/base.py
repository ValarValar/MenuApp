from abc import ABC, abstractmethod
from typing import Union

from pydantic.types import UUID

from db.cache.base import AbstractCache
from db.uow import SqlModelUnitOfWork


class ServiceBase(ABC):
    def __init__(self, cache: AbstractCache, uow: SqlModelUnitOfWork):
        self.cache = cache
        self.uow = uow

    @property
    @abstractmethod
    def cache_list_key(self) -> Union[str, UUID]:
        pass

    @property
    @abstractmethod
    def cache_list_keys_to_clear(self) -> list[Union[str, UUID]]:
        pass

from abc import ABC, abstractmethod
from typing import Optional, Union

__all__ = (
    "AbstractCache",
    "get_cache",
)

from pydantic.types import UUID


class AbstractCache(ABC):
    def __init__(self, cache_instance):
        self.cache = cache_instance

    @abstractmethod
    def get(self, key: Union[str, UUID]):
        pass

    @abstractmethod
    def set(
        self,
        key: Union[str, UUID],
        value: Union[bytes, str],
        expire: int = 600,
    ):
        pass

    @abstractmethod
    def delete(self, key: Union[str, UUID]):
        self.cache.delete(key)

    @abstractmethod
    def delete_list_keys(self, keys: list[Union[str, UUID]]):
        for key in keys:
            self.delete(key)

    @abstractmethod
    def close(self):
        pass


cache: Optional[AbstractCache] = None


# Функция понадобится при внедрении зависимостей
def get_cache() -> Optional[AbstractCache]:
    return cache

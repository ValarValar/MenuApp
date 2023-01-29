from abc import ABC, abstractmethod
from typing import Optional, Union

__all__ = (
    "AbstractCache",
    "get_cache",
)


class AbstractCache(ABC):
    def __init__(self, cache_instance):
        self.cache = cache_instance

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(
            self,
            key: str,
            value: Union[bytes, str],
            expire: int = 600,
    ):
        pass

    @abstractmethod
    def delete(self, key: str):
        self.cache.delete(key)

    @abstractmethod
    def close(self):
        pass


cache: Optional[AbstractCache] = None


# Функция понадобится при внедрении зависимостей
def get_cache() -> AbstractCache:
    return cache

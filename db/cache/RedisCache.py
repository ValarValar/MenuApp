from typing import NoReturn, Optional, Union

__all__ = ("CacheRedis",)

from core.config import get_settings
from db.cache.base import AbstractCache


class CacheRedis(AbstractCache):
    def get(self, key: str) -> Optional[dict]:
        return self.cache.get(name=key)

    def set(
            self,
            key: str,
            value: Union[bytes, str],
            expire: int = get_settings().CACHE_EXPIRE_IN_SECONDS,
    ):
        self.cache.set(name=key, value=value, ex=expire)

    def close(self) -> NoReturn:
        self.cache.close()



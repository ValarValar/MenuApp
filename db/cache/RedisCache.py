from typing import NoReturn, Optional, Union

__all__ = ("CacheRedis",)

import redis
from fastapi import Depends
from pydantic.main import BaseModel

from core.config import get_settings, Settings
from db.cache.base import AbstractCache


class CacheRedis(AbstractCache):
    def get(self, key: str) -> Optional[dict]:
        return self.cache.get(name=key)

    def set(
            self,
            key: str,
            value: Union[bytes, str],
            expire: int = get_settings().REDIS_CACHE_EXPIRE_IN_SECONDS, ):
        self.cache.set(name=key, value=value, ex=expire)

    def delete(self, key):
        self.cache.delete(key)

    def close(self) -> NoReturn:
        self.cache.close()


def get_redis_cache(settings: Settings = Depends(get_settings)):
    redis_cache = CacheRedis(
        redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=1, decode_responses=True,
        )
    )
    return redis_cache

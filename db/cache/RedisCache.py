from typing import Optional, Union

from fastapi import Depends
from redis.asyncio.client import Redis

from core.config import Settings, get_settings
from db.cache.base import AbstractCache


class CacheRedis(AbstractCache):
    async def get(self, key: str) -> Optional[dict]:
        return await self.cache.get(name=key)

    async def set(
        self,
        key: str,
        value: Union[bytes, str],
        expire: int = get_settings().REDIS_CACHE_EXPIRE_IN_SECONDS,
    ):
        await self.cache.set(name=key, value=value, ex=expire)

    async def delete(self, key):
        await self.cache.delete(key)

    async def close(self):
        await self.cache.close()


async def get_redis_cache(settings: Settings = Depends(get_settings)):
    redis_cache = CacheRedis(
        Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=1,
            decode_responses=True,
        ),
    )
    return redis_cache

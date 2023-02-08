from typing import Optional, Union

from fastapi import Depends
from pydantic.types import UUID
from redis.asyncio.client import Redis

from core.config import Settings, get_settings
from db.cache.base import AbstractCache


class CacheRedis(AbstractCache):
    async def get(self, key: Union[str, UUID]) -> Optional[dict]:
        key = str(key)
        return await self.cache.get(name=key)

    async def set(
        self,
        key: Union[str, UUID],
        value: Union[bytes, str],
        expire: int = get_settings().REDIS_CACHE_EXPIRE_IN_SECONDS,
    ):
        key = str(key)
        await self.cache.set(name=key, value=value, ex=expire)

    async def delete(self, key: Union[str, UUID]):
        key = str(key)
        await self.cache.delete(key)

    async def delete_list_keys(self, keys: list[Union[str, UUID]]):
        for key in keys:
            key = str(key)
            await self.delete(key)

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

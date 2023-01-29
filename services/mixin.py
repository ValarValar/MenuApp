from db.cache.base import AbstractCache
from db.uow import SqlModelUnitOfWork


class ServiceMixin:
    def __init__(self, cache: AbstractCache, uow: SqlModelUnitOfWork):
        self.cache = cache
        self.uow = uow

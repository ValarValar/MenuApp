from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

__all__ = ("get_session",)

from sqlalchemy.orm import sessionmaker

from core.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.POSTGRES_URL, echo=True, future=True)


async def get_session():
    async_session = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session

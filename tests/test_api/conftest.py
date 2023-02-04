import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from db.db import get_session
from main import app
from tests.config import get_test_settings

settings = get_test_settings()

engine = create_async_engine(settings.POSTGRES_TEST_URL, future=True)


async def override_get_session():
    async_session = sessionmaker(
        engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
@pytest.fixture(scope="function", autouse=True)
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest.mark.anyio
@pytest.fixture(scope="function")
async def test_client():
    async with AsyncClient(app=app, base_url="http://") as client:
        yield client

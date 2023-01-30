import pytest
from sqlalchemy_utils import create_database, database_exists
from sqlmodel import Session, SQLModel, create_engine
from starlette.testclient import TestClient

from core.config import get_settings
from db.db import get_session
from main import app

settings = get_settings()

engine = create_engine(settings.POSTGRES_TEST_URL)
database_exists = database_exists(engine.url)
if not database_exists:
    create_database(engine.url)


def override_get_session():
    with Session(bind=engine, autocommit=False, autoflush=False) as session:
        yield session


@pytest.fixture(scope='class')
def test_db():
    SQLModel.metadata.create_all(bind=engine)
    yield
    SQLModel.metadata.drop_all(bind=engine)


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope='class')
def test_client():
    with TestClient(app) as client:
        yield client

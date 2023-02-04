from functools import lru_cache

from dotenv import find_dotenv
from pydantic import BaseSettings


class TestsSettings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    APP_NAME: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_TEST_URL: str

    class Config:
        env_file = find_dotenv(filename=".env.tests", usecwd=True)


@lru_cache
def get_test_settings():
    return TestsSettings()

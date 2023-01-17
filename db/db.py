from sqlmodel import Session, create_engine

__all__ = ("get_session",)

from core.config import get_settings

settings = get_settings()

engine = create_engine(settings.POSTGRES_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session

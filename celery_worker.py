import asyncio

from celery import Celery
from pyexcel import save_as
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import get_settings
from db.db import engine
from db.repositories.data import DataRepository

settings = get_settings()

celery = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BACKEND_URL,
)


def create_session() -> AsyncSession:
    session = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    return session()


def create_filename(task_id: str) -> str:
    result = f"{settings.APP_MEDIA_PATH}/{task_id}_data_dump.xlsx"
    return result


async def convert_data(task_id: str) -> str:
    data_repo = DataRepository(create_session())
    data: dict = await data_repo.dump_data()
    filename = create_filename(task_id)
    data_to_excel: list = []
    if data["menus"] is None:
        save_as(array=data_to_excel, dest_file_name=filename, encoding="utf-8")
        return filename

    for menu_num, menu in enumerate(data["menus"]):
        menu_data = menu["menu"]
        data_to_excel.append(
            [menu_num + 1, menu_data["title"], menu_data["description"]]
        )
        for submenu_num, submenu in enumerate(menu["submenus"]):
            submenu_data = submenu["submenu"]
            data_to_excel.append(
                [
                    "",
                    submenu_num + 1,
                    submenu_data["title"],
                    submenu_data["description"],
                ]
            )
            for dish_num, dish in enumerate(submenu["dishes"]):
                dish_data = dish["dish"]
                data_to_excel.append(
                    [
                        "",
                        "",
                        dish_num + 1,
                        dish_data["title"],
                        dish_data["description"],
                        dish_data["price"],
                    ]
                )

    save_as(array=data_to_excel, dest_file_name=filename, encoding="utf-8")
    return filename


@celery.task(bind=True, name="data_to_excel_task", track_started=True)
def data_to_excel_task(
    self,
):
    result = asyncio.run(convert_data(self.request.id))
    return result

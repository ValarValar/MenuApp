import http

from celery.result import AsyncResult
from fastapi import APIRouter, Depends
from starlette.responses import FileResponse, JSONResponse, Response

from api.v1.schemas.service import TestDataBase
from celery_worker import data_to_excel_task
from services.data_service import DataService, get_data_service

router = APIRouter()


@router.post(
    path="/",
    summary="Fill db with test data",
    tags=["data"],
    response_model=TestDataBase,
    status_code=http.HTTPStatus.OK,
)
async def fill_db_with_test_data(
    test_data_service: DataService = Depends(get_data_service),
):
    return await test_data_service.fill_db_with_test_data()


@router.post(
    path="/tasks",
    summary="Create convert data to excel task",
    tags=["data"],
    status_code=http.HTTPStatus.CREATED,
)
async def create_convert_task():
    task = data_to_excel_task.delay()
    return JSONResponse({"task_id": task.id})


@router.get(
    path="/tasks/{task_id}",
    summary="Get data conversion task result",
    tags=["data"],
    status_code=http.HTTPStatus.OK,
)
async def get_task_status(task_id: str) -> Response:
    task_result = AsyncResult(task_id)
    if task_result.ready():
        return FileResponse(
            path=task_result.result,
            filename=task_result.result,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    result = JSONResponse(
        {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result,
        }
    )
    return result

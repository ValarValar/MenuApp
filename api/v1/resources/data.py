import http

from fastapi import APIRouter, Depends

from api.v1.schemas.service import TestDataBase
from services.data_service import DataService, get_data_service

router = APIRouter()


@router.post(
    path="/",
    summary="Fill db with test data",
    tags=["data"],
    response_model=TestDataBase,
    status_code=http.HTTPStatus.OK,
)
async def fill_db_with_test_data(test_data_service: DataService = Depends(get_data_service)):
    return await test_data_service.fill_db_with_test_data()

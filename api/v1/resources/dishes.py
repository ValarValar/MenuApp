import http

from fastapi import APIRouter, Depends
from pydantic.types import UUID

from api.v1.schemas.dishes import DishBase, DishDetail, DishList, DishUpdate
from api.v1.schemas.service import DeleteBase
from services.dish_service import DishService, get_dish_service

router = APIRouter()


@router.post(
    path="/",
    summary="Create Dish",
    response_model=DishDetail,
    status_code=http.HTTPStatus.CREATED,
)
async def create_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish: DishBase,
    dish_service: DishService = Depends(get_dish_service),
):
    return await dish_service.create(dish, menu_id, submenu_id)


@router.get(
    path="/",
    summary="List dishes",
    response_model=DishList,
    status_code=http.HTTPStatus.OK,
)
async def list_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_service: DishService = Depends(get_dish_service),
):
    return await dish_service.get_list(menu_id, submenu_id)


@router.get(
    path="/{dish_id}",
    summary="Detailed dish",
    response_model=DishDetail,
    status_code=http.HTTPStatus.OK,
)
async def get_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_service: DishService = Depends(get_dish_service),
):
    return await dish_service.get_detail(menu_id, submenu_id, dish_id)


@router.patch(
    path="/{dish_id}",
    summary="Update dish",
    response_model=DishDetail,
    status_code=http.HTTPStatus.OK,
)
async def update_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    new_dish: DishUpdate,
    dish_service: DishService = Depends(get_dish_service),
):
    return await dish_service.update(menu_id, submenu_id, dish_id, new_dish)


@router.delete(
    path="/{dish_id}",
    summary="Delete dish",
    response_model=DeleteBase,
    status_code=http.HTTPStatus.OK,
)
async def delete_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_service: DishService = Depends(get_dish_service),
):
    return await dish_service.delete(menu_id, submenu_id, dish_id)

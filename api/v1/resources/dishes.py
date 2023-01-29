from fastapi import APIRouter, Depends

from api.v1.schemas.dishes import DishCreate, DishUpdate, DishBase, DishList
from services.dish_service import DishService, get_dish_service

router = APIRouter()


@router.post(
    path="/",
    summary="Create Dish",
    response_model=DishCreate,
    status_code=201
)
def create_dish(
        menu_id: str,
        submenu_id: str,
        dish: DishBase,
        dish_service: DishService = Depends(get_dish_service),
):
    return dish_service.create(dish, menu_id, submenu_id)


@router.get(
    path="/",
    summary="List dishes",
    response_model=DishList,
)
def list_dish(
        menu_id: str,
        submenu_id: str,
        dish_service: DishService = Depends(get_dish_service),
):
    return dish_service.get_list(menu_id, submenu_id)


@router.get(
    path="/{dish_id}",
    summary="Detailed dish",
    response_model=DishCreate
)
def get_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        dish_service: DishService = Depends(get_dish_service),
):
    return dish_service.get_detail(menu_id, submenu_id, dish_id)


@router.patch(
    path="/{dish_id}",
    summary="Update dish",
    response_model=DishCreate
)
def update_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        new_dish: DishUpdate,
        dish_service: DishService = Depends(get_dish_service)
):
    return dish_service.update(menu_id, submenu_id, dish_id, new_dish)


@router.delete(
    path="/{dish_id}",
    summary="Delete dish",
)
def delete_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        dish_service: DishService = Depends(get_dish_service)
):
    return dish_service.delete(menu_id, submenu_id, dish_id)

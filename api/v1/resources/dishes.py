from fastapi import APIRouter, Depends, HTTPException

from api.v1.schemas.dishes import DishCreate, DishUpdate, DishBase
from db.dish_db_service import DishDbService, get_dish_db_service
from db.submenu_db_service import SubmenuDbService, get_submenu_db_service

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
        dish_db: DishDbService = Depends(get_dish_db_service),
):
    return dish_db.create_dish(dish, menu_id, submenu_id)


@router.get(
    path="/",
    summary="List dishes",
    response_model=list[DishBase],
)
def list_dish(
        menu_id: str,
        submenu_id: str,
        dish_db: DishDbService = Depends(get_dish_db_service),
):
    return dish_db.list_dishes(menu_id, submenu_id)


@router.get(
    path="/{dish_id}",
    summary="Detailed dish",
    response_model=DishCreate
)
def get_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        dish_db: DishDbService = Depends(get_dish_db_service),
):
    return dish_db.get_dish_by_ids(menu_id, submenu_id, dish_id)


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
        dish_db: DishDbService = Depends(get_dish_db_service)
):
    return dish_db.update_dish(menu_id, submenu_id, dish_id, new_dish)


@router.delete(
    path="/{dish_id}",
    summary="Delete dish",
)
def delete_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        dish_db: DishDbService = Depends(get_dish_db_service)
):
    deleted_dish = dish_db.delete_dish(menu_id, submenu_id, dish_id)
    if not deleted_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    return {"ok": deleted_dish}

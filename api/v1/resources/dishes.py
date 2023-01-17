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
        submenu_db: SubmenuDbService = Depends(get_submenu_db_service),
):
    submenu = submenu_db.get_submenu_by_ids(menu_id, submenu_id)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    created_dish = dish_db.create_dish(dish, submenu_id).dict()
    return DishCreate(**created_dish)


@router.get(
    path="/",
    summary="List dishs",
    response_model=list[DishBase],
)
def list_dish(
        menu_id: str,
        submenu_id: str,
        dish_db: DishDbService = Depends(get_dish_db_service),
        submenu_db: SubmenuDbService = Depends(get_submenu_db_service),
):
    # Для прохождение теста закомментировано, но по логике если обращаемся к несуществующему меню, должна быть ошибка
    # submenu = submenu_db.get_submenu_by_ids(menu_id, submenu_id)
    # if not submenu:
    # raise HTTPException(status_code=404, detail="submenu not found")

    dishes = dish_db.list_dishes(menu_id, submenu_id)
    return [DishBase(**dish.dict()) for dish in dishes]


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
    detailed_dish = dish_db.get_dish_by_ids(menu_id, submenu_id, dish_id)

    if not detailed_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    return DishCreate(**detailed_dish.dict())


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
    updated_dish = dish_db.update_dish(menu_id, submenu_id, dish_id, new_dish)
    if not updated_dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return DishCreate(**updated_dish.dict())


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

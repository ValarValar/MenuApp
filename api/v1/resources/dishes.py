from fastapi import APIRouter, Depends, HTTPException

from api.v1.schemas.dishes import DishCreate, DishUpdate, DishBase
from db.dish_db_service import DishDbService, get_dish_db_service

router = APIRouter()


@router.post(
    path="/",
    summary="Create Dish",
    response_model=DishCreate,
    status_code=201
)
def create_dish(dish: DishBase, dish_db: DishDbService = Depends(get_dish_db_service)):
    created_dish = dish_db.create_item(dish).dict()
    return DishCreate(**created_dish)


@router.get(
    path="/",
    summary="List dishs",
    response_model=list[DishBase],
)
def list_dish(dish_db: DishDbService = Depends(get_dish_db_service)):
    dishs = dish_db.list_items()
    return [DishBase(**dish.dict()) for dish in dishs]


@router.get(
    path="/{dish_id}",
    summary="Detailed dish",
    response_model=DishCreate
)
def get_dish(
        dish_id: str,
        dish_db: DishDbService = Depends(get_dish_db_service)
):
    detailed_dish = dish_db.get_item_by_id(dish_id)
    if detailed_dish:
        return DishCreate(**detailed_dish.dict())
    else:
        raise HTTPException(status_code=404, detail="dish not found")


@router.patch(
    path="/{dish_id}",
    summary="Update dish",
    response_model=DishCreate
)
def update_dish(
        dish_id: str,
        new_dish: DishUpdate,
        dish_db: DishDbService = Depends(get_dish_db_service)
):
    updated_dish = dish_db.update_item(dish_id, new_dish)
    if updated_dish:
        return DishCreate(**updated_dish.dict())
    else:
        raise HTTPException(status_code=404, detail="dish not found")


@router.delete(
    path="/{dish_id}",
    summary="Delete dish",
)
def delete_dish(
        dish_id: str,
        dish_db: DishDbService = Depends(get_dish_db_service)
):
    deleted_dish = dish_db.delete_item(dish_id)
    if deleted_dish:
        return {"ok": deleted_dish}
    else:
        raise HTTPException(status_code=404, detail="dish not found")

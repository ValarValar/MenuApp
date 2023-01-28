from fastapi import APIRouter, Depends

from api.v1.schemas.menus import MenuCreate, MenuBase, MenuUpdate, MenuWithCount
from db.menu_db_service import get_menu_db_service, MenuDbService

router = APIRouter()


@router.post(
    path="/",
    summary="Create menu",
    tags=["menus"],
    response_model=MenuCreate,
    status_code=201
)
def create_menu(menu: MenuBase, menu_db: MenuDbService = Depends(get_menu_db_service)):
    return menu_db.create_menu(menu)


@router.get(
    path="/",
    summary="List menus",
    tags=["menus"],
    response_model=list[MenuWithCount],
)
def list_menu(menu_db: MenuDbService = Depends(get_menu_db_service)):
    return menu_db.list_menu()


@router.get(
    path="/{menu_id}",
    summary="Detailed menu",
    tags=["menus"],
    response_model=MenuWithCount
)
def get_menu(
        menu_id: str,
        menu_db: MenuDbService = Depends(get_menu_db_service)
):
    return menu_db.get_menu_by_id_with_counts(menu_id)


@router.patch(
    path="/{menu_id}",
    summary="Update menu",
    tags=["menus"],
    response_model=MenuCreate
)
def update_menu(
        menu_id: str,
        new_menu: MenuUpdate,
        menu_db: MenuDbService = Depends(get_menu_db_service)
):
    return menu_db.update_menu(menu_id, new_menu)


@router.delete(
    path="/{menu_id}",
    summary="Delete menu",
    tags=["menus"]
)
def delete_menu(
        menu_id: str,
        menu_db: MenuDbService = Depends(get_menu_db_service)
):
    return menu_db.delete_menu(menu_id)

from fastapi import APIRouter, Depends

from api.v1.schemas.menus import MenuCreate, MenuBase, MenuUpdate, MenuList, MenuDetail
from db.menu_service import get_menu_service, MenuService

router = APIRouter()


@router.post(
    path="/",
    summary="Create menu",
    tags=["menus"],
    response_model=MenuCreate,
    status_code=201
)
def create_menu(menu: MenuBase, menu_service: MenuService = Depends(get_menu_service)):
    return menu_service.create(menu)


@router.get(
    path="/",
    summary="List menus",
    tags=["menus"],
    response_model=MenuList
)
def list_menu(menu_service: MenuService = Depends(get_menu_service)):
    return menu_service.list()


@router.get(
    path="/{menu_id}",
    summary="Detailed menu",
    tags=["menus"],
    response_model=MenuDetail
)
def get_menu(
        menu_id: str,
        menu_service: MenuService = Depends(get_menu_service)
):
    return menu_service.get(menu_id)


@router.patch(
    path="/{menu_id}",
    summary="Update menu",
    tags=["menus"],
    response_model=MenuCreate
)
def update_menu(
        menu_id: str,
        new_menu: MenuUpdate,
        menu_service: MenuService = Depends(get_menu_service)
):
    return menu_service.update(menu_id, new_menu)


@router.delete(
    path="/{menu_id}",
    summary="Delete menu",
    tags=["menus"]
)
def delete_menu(
        menu_id: str,
        menu_service: MenuService = Depends(get_menu_service)
):
    return menu_service.delete(menu_id)

from fastapi import APIRouter, Depends, HTTPException

from api.v1.schemas.menus import MenuCreate, MenuBase, UpdateMenu
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
    created_menu = menu_db.create_menu(menu).dict()
    return MenuCreate(**created_menu)


@router.get(
    path="/",
    summary="List menus",
    tags=["menus"],
    response_model=list[MenuBase],
)
def list_menu(menu_db: MenuDbService = Depends(get_menu_db_service)):
    menus = menu_db.list_menu()
    return [MenuBase(**menu.dict()) for menu in menus]


@router.get(
    path="/{menu_id}",
    summary="Detailed menu",
    tags=["menus"],
    response_model=MenuCreate
)
def get_menu(
        menu_id: str,
        menu_db: MenuDbService = Depends(get_menu_db_service)
):
    detailed_menu = menu_db.get_menu_by_id(menu_id)
    if detailed_menu:
        return MenuCreate(**detailed_menu.dict())
    else:
        raise HTTPException(status_code=404, detail="menu not found")


@router.patch(
    path="/{menu_id}",
    summary="Update menu",
    tags=["menus"],
    response_model=MenuCreate
)
def update_menu(
        menu_id: str,
        new_menu: UpdateMenu,
        menu_db: MenuDbService = Depends(get_menu_db_service)
):
    updated_menu = menu_db.update_menu(menu_id, new_menu)
    if updated_menu:
        return MenuCreate(**updated_menu.dict())
    else:
        raise HTTPException(status_code=404, detail="menu not found")


@router.delete(
    path="/{menu_id}",
    summary="Delete menu",
    tags=["menus"]
)
def delete_menu(
        menu_id: str,
        menu_db: MenuDbService = Depends(get_menu_db_service)
):
    deleted_menu = menu_db.delete_menu(menu_id)
    if deleted_menu:
        return {"ok": deleted_menu}
    else:
        raise HTTPException(status_code=404, detail="menu not found")

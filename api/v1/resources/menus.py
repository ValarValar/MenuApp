from fastapi import APIRouter, Depends, HTTPException

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
    response_model=MenuWithCount
)
def get_menu(
        menu_id: str,
        menu_db: MenuDbService = Depends(get_menu_db_service)
):
    detailed_menu = menu_db.get_menu_by_id(menu_id)
    if not detailed_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    submenus = detailed_menu.submenus
    submenus_count = len(detailed_menu.submenus)
    dishes_count = sum([len(submenu.dishes) for submenu in submenus])
    response_model = MenuWithCount(
        submenus_count=submenus_count,
        dishes_count=dishes_count,
        **detailed_menu.dict()
    )
    return response_model



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
    updated_menu = menu_db.update_menu(menu_id, new_menu)
    if not updated_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return MenuCreate(**updated_menu.dict())


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
    if not deleted_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return {"ok": deleted_menu}

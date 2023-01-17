from fastapi import APIRouter, Depends, HTTPException

from api.v1.schemas.submenus import SubmenuCreate, SubmenuUpdate, SubmenuBase, SubmenuWithCount
from db.menu_db_service import MenuDbService, get_menu_db_service
from db.submenu_db_service import SubmenuDbService, get_submenu_db_service

router = APIRouter()


@router.post(
    path="/",
    summary="Create Submenu",
    tags=["submenus"],
    response_model=SubmenuCreate,
    status_code=201
)
def create_submenu(
        menu_id: str,
        submenu: SubmenuBase,
        submenu_db: SubmenuDbService = Depends(get_submenu_db_service),
        menu_db: MenuDbService = Depends(get_menu_db_service)
):
    menu = menu_db.get_menu_by_id(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")

    created_submenu = submenu_db.create_submenu(submenu, menu_id).dict()
    return SubmenuCreate(**created_submenu)


@router.get(
    path="/",
    summary="List submenus",
    tags=["submenus"],
    response_model=list[SubmenuBase],
)
def list_submenu(
        menu_id: str,
        submenu_db: SubmenuDbService = Depends(get_submenu_db_service),
        menu_db: MenuDbService = Depends(get_menu_db_service)
):
    menu = menu_db.get_menu_by_id(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")

    submenus = submenu_db.list_submenus(menu_id)

    return [SubmenuBase(**submenu.dict()) for submenu in submenus]


@router.get(
    path="/{submenu_id}",
    summary="Detailed submenu",
    tags=["submenus"],
    response_model=SubmenuWithCount
)
def get_submenu(
        menu_id: str,
        submenu_id: str,
        submenu_db: SubmenuDbService = Depends(get_submenu_db_service),
):
    detailed_submenu = submenu_db.get_submenu_by_ids(menu_id, submenu_id)
    if not detailed_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    dishes_count = len(detailed_submenu.dishes)
    return SubmenuWithCount(dishes_count=dishes_count, **detailed_submenu.dict())


@router.patch(
    path="/{submenu_id}",
    summary="Update submenu",
    tags=["submenus"],
    response_model=SubmenuCreate
)
def update_submenu(
        menu_id: str,
        submenu_id: str,
        new_submenu: SubmenuUpdate,
        submenu_db: SubmenuDbService = Depends(get_submenu_db_service)
):
    updated_submenu = submenu_db.update_submenu(menu_id, submenu_id, new_submenu)

    if not updated_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    return SubmenuCreate(**updated_submenu.dict())


@router.delete(
    path="/{submenu_id}",
    summary="Delete submenu",
    tags=["submenus"]
)
def delete_submenu(
        menu_id: str,
        submenu_id: str,
        submenu_db: SubmenuDbService = Depends(get_submenu_db_service)
):
    deleted_submenu = submenu_db.delete_submenu(menu_id, submenu_id)
    if deleted_submenu:
        return {"ok": deleted_submenu}
    else:
        raise HTTPException(status_code=404, detail="submenu not found")

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
):
    return submenu_db.create_submenu(submenu, menu_id)


@router.get(
    path="/",
    summary="List submenus",
    tags=["submenus"],
    response_model=list[SubmenuWithCount],
)
def list_submenu(
        menu_id: str,
        submenu_db: SubmenuDbService = Depends(get_submenu_db_service)
):
    return submenu_db.list_submenus(menu_id)


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
    return submenu_db.get_submenu_by_ids(menu_id, submenu_id)


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
    return submenu_db.update_submenu(menu_id, submenu_id, new_submenu)


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
    return submenu_db.delete_submenu(menu_id, submenu_id)

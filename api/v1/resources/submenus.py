from fastapi import APIRouter, Depends, HTTPException

from api.v1.schemas.submenus import SubmenuCreate, SubmenuUpdate, SubmenuBase, SubmenuForCreate
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
        submenu_db: SubmenuDbService = Depends(get_submenu_db_service)):
    submenu_with_menu_id = SubmenuForCreate(menu_id=menu_id, **submenu.dict())
    created_submenu = submenu_db.create_item(submenu_with_menu_id).dict()
    return SubmenuCreate(**created_submenu)


@router.get(
    path="/",
    summary="List submenus",
    tags=["submenus"],
    response_model=list[SubmenuBase],
)
def list_submenu(submenu_db: SubmenuDbService = Depends(get_submenu_db_service)):
    submenus = submenu_db.list_items()
    return [SubmenuBase(**submenu.dict()) for submenu in submenus]


@router.get(
    path="/{submenu_id}",
    summary="Detailed submenu",
    tags=["submenus"],
    response_model=SubmenuCreate
)
def get_submenu(
        submenu_id: str,
        submenu_db: SubmenuDbService = Depends(get_submenu_db_service)
):
    detailed_submenu = submenu_db.get_item_by_id(submenu_id)
    if detailed_submenu:
        return SubmenuCreate(**detailed_submenu.dict())
    else:
        raise HTTPException(status_code=404, detail="submenu not found")


@router.patch(
    path="/{submenu_id}",
    summary="Update submenu",
    tags=["submenus"],
    response_model=SubmenuCreate
)
def update_submenu(
        submenu_id: str,
        new_submenu: SubmenuUpdate,
        menu_id: str,
        submenu_db: SubmenuDbService = Depends(get_submenu_db_service)
):
    updated_submenu = submenu_db.update_item(submenu_id, new_submenu)
    if updated_submenu:
        return SubmenuCreate(**updated_submenu.dict())
    else:
        raise HTTPException(status_code=404, detail="submenu not found")


@router.delete(
    path="/{submenu_id}",
    summary="Delete submenu",
    tags=["submenus"]
)
def delete_submenu(
        submenu_id: str,
        submenu_db: SubmenuDbService = Depends(get_submenu_db_service)
):
    deleted_submenu = submenu_db.delete_item(submenu_id)
    if deleted_submenu:
        return {"ok": deleted_submenu}
    else:
        raise HTTPException(status_code=404, detail="submenu not found")

import http

from fastapi import APIRouter, Depends

from api.v1.schemas.service import DeleteBase
from api.v1.schemas.submenus import (
    SubmenuBase,
    SubmenuCreate,
    SubmenuDetail,
    SubmenuList,
    SubmenuUpdate,
)
from services.submenu_service import SubmenuService, get_submenu_service

router = APIRouter()


@router.post(
    path="/",
    summary="Create Submenu",
    tags=["submenus"],
    response_model=SubmenuCreate,
    status_code=http.HTTPStatus.CREATED,
)
async def create_submenu(
    menu_id: str,
    submenu: SubmenuBase,
    submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return await submenu_service.create(submenu, menu_id)


@router.get(
    path="/",
    summary="List submenus",
    tags=["submenus"],
    response_model=SubmenuList,
    status_code=http.HTTPStatus.OK,
)
async def list_submenu(
    menu_id: str,
    submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return await submenu_service.get_list(menu_id)


@router.get(
    path="/{submenu_id}",
    summary="Detailed submenu",
    tags=["submenus"],
    response_model=SubmenuDetail,
    status_code=http.HTTPStatus.OK,
)
async def get_submenu(
    menu_id: str,
    submenu_id: str,
    submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return await submenu_service.get_detail(menu_id, submenu_id)


@router.patch(
    path="/{submenu_id}",
    summary="Update submenu",
    tags=["submenus"],
    response_model=SubmenuCreate,
    status_code=http.HTTPStatus.OK,
)
async def update_submenu(
    menu_id: str,
    submenu_id: str,
    new_submenu: SubmenuUpdate,
    submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return await submenu_service.update(menu_id, submenu_id, new_submenu)


@router.delete(
    path="/{submenu_id}",
    summary="Delete submenu",
    tags=["submenus"],
    response_model=DeleteBase,
    status_code=http.HTTPStatus.OK,
)
async def delete_submenu(
    menu_id: str,
    submenu_id: str,
    submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return await submenu_service.delete(menu_id, submenu_id)

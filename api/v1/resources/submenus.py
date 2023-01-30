import http

from fastapi import APIRouter, Depends

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
    path='/',
    summary='Create Submenu',
    tags=['submenus'],
    response_model=SubmenuCreate,
    status_code=http.HTTPStatus.CREATED,
)
def create_submenu(
        menu_id: str,
        submenu: SubmenuBase,
        submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return submenu_service.create(submenu, menu_id)


@router.get(
    path='/',
    summary='List submenus',
    tags=['submenus'],
    response_model=SubmenuList,
    status_code=http.HTTPStatus.OK,
)
def list_submenu(
        menu_id: str,
        submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return submenu_service.get_list(menu_id)


@router.get(
    path='/{submenu_id}',
    summary='Detailed submenu',
    tags=['submenus'],
    response_model=SubmenuDetail,
    status_code=http.HTTPStatus.OK,
)
def get_submenu(
        menu_id: str,
        submenu_id: str,
        submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return submenu_service.get_detail(menu_id, submenu_id)


@router.patch(
    path='/{submenu_id}',
    summary='Update submenu',
    tags=['submenus'],
    response_model=SubmenuCreate,
    status_code=http.HTTPStatus.OK,
)
def update_submenu(
        menu_id: str,
        submenu_id: str,
        new_submenu: SubmenuUpdate,
        submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return submenu_service.update(menu_id, submenu_id, new_submenu)


@router.delete(
    path='/{submenu_id}',
    summary='Delete submenu',
    tags=['submenus'],
    response_model=dict,
    status_code=http.HTTPStatus.OK,
)
def delete_submenu(
        menu_id: str,
        submenu_id: str,
        submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return submenu_service.delete(menu_id, submenu_id)

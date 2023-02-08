import http

from fastapi import APIRouter, Depends
from pydantic.types import UUID

from api.v1.schemas.menus import MenuBase, MenuCreate, MenuDetail, MenuList, MenuUpdate
from api.v1.schemas.service import DeleteBase
from services.menu_service import MenuService, get_menu_service

router = APIRouter()


@router.post(
    path="/",
    summary="Create menu",
    tags=["menus"],
    response_model=MenuCreate,
    status_code=http.HTTPStatus.CREATED,
)
async def create_menu(
    menu: MenuBase, menu_service: MenuService = Depends(get_menu_service)
):
    return await menu_service.create(menu)


@router.get(
    path="/",
    summary="List menus",
    tags=["menus"],
    response_model=MenuList,
    status_code=http.HTTPStatus.OK,
)
async def list_menu(menu_service: MenuService = Depends(get_menu_service)):
    return await menu_service.get_list()


@router.get(
    path="/{menu_id}",
    summary="Detailed menu",
    tags=["menus"],
    response_model=MenuDetail,
    status_code=http.HTTPStatus.OK,
)
async def get_menu(
    menu_id: UUID,
    menu_service: MenuService = Depends(get_menu_service),
):
    return await menu_service.get_detail(menu_id)


@router.patch(
    path="/{menu_id}",
    summary="Update menu",
    tags=["menus"],
    response_model=MenuCreate,
    status_code=http.HTTPStatus.OK,
)
async def update_menu(
    menu_id: UUID,
    new_menu: MenuUpdate,
    menu_service: MenuService = Depends(get_menu_service),
):
    return await menu_service.update(menu_id, new_menu)


@router.delete(
    path="/{menu_id}",
    summary="Delete menu",
    tags=["menus"],
    response_model=DeleteBase,
    status_code=http.HTTPStatus.OK,
)
async def delete_menu(
    menu_id: UUID,
    menu_service: MenuService = Depends(get_menu_service),
):
    return await menu_service.delete(menu_id)

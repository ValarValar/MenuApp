from uuid import UUID

import pytest
from httpx import AsyncClient

from main import app

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="function")
async def menu_id(test_client: AsyncClient, test_db):
    base_url = app.url_path_for("create_menu")
    new_menu = {
        "title": "My menu 1",
        "description": "My menu description 1",
    }
    response = await test_client.post(base_url, json=new_menu)
    menu_id = response.json()["id"]
    return menu_id


async def test_empty_submenus(test_client: AsyncClient, menu_id):
    base_url = app.url_path_for("list_submenu", menu_id=menu_id)
    response = await test_client.get(base_url)

    assert response.status_code == 200
    expected_answer: list = []
    assert expected_answer == response.json()


async def test_submenu_create(test_client: AsyncClient, menu_id):
    base_url = app.url_path_for("create_submenu", menu_id=menu_id)
    new_submenu = {
        "title": "My submenu 1",
        "description": "My submenu description 1",
    }
    response = await test_client.post(base_url, json=new_submenu)

    assert response.status_code == 201

    expected_answer = {
        "title": "My submenu 1",
        "description": "My submenu description 1",
    }
    response_dict = response.json()
    assert expected_answer["title"] == response_dict["title"]
    assert expected_answer["description"] == response_dict["description"]
    assert isinstance(UUID(response_dict["id"]), UUID)


async def test_detailed_submenu(test_client: AsyncClient, menu_id):
    base_url = app.url_path_for("create_submenu", menu_id=menu_id)
    new_submenu = {
        "title": "My submenu 1",
        "description": "My submenu description 1",
    }
    response = await test_client.post(base_url, json=new_submenu)

    submenu_id = response.json()["id"]
    url = app.url_path_for(
        "get_submenu",
        menu_id=menu_id,
        submenu_id=submenu_id,
    )

    response = await test_client.get(url)
    expected_answer = {
        "title": "My submenu 1",
        "description": "My submenu description 1",
        "dishes_count": 0,
        "id": submenu_id,
    }
    response_dict = response.json()
    assert response.status_code == 200
    assert expected_answer["title"] == response_dict["title"]
    assert expected_answer["description"] == response_dict["description"]
    assert expected_answer["dishes_count"] == response_dict["dishes_count"]
    assert expected_answer["id"] == response_dict["id"]


async def test_detailed_submenu_invalid(test_client: AsyncClient, menu_id):
    base_url = app.url_path_for("create_submenu", menu_id=menu_id)
    new_submenu = {
        "title": "My submenu 1",
        "description": "My submenu description 1",
    }
    response = await test_client.post(base_url, json=new_submenu)

    submenu_id = response.json()["id"]
    submenu_id = submenu_id[:-5] + "1" * 5
    url = app.url_path_for(
        "get_submenu",
        menu_id=menu_id,
        submenu_id=submenu_id,
    )

    response = await test_client.get(url)
    assert response.status_code == 404


async def test_delete_submenu(test_client: AsyncClient, menu_id):
    base_url = app.url_path_for("create_submenu", menu_id=menu_id)
    new_submenu = {
        "title": "My submenu 1",
        "description": "My submenu description 1",
    }
    response = await test_client.post(base_url, json=new_submenu)

    submenu_id = response.json()["id"]
    url = app.url_path_for(
        "delete_submenu",
        menu_id=menu_id,
        submenu_id=submenu_id,
    )

    response = await test_client.delete(url)
    expected_answer = {
        "deleted": True,
    }
    assert response.status_code == 200
    assert expected_answer == response.json()


async def test_delete_submenu_invalid(test_client: AsyncClient, menu_id):
    base_url = app.url_path_for("create_submenu", menu_id=menu_id)
    new_submenu = {
        "title": "My submenu 1",
        "description": "My submenu description 1",
    }
    response = await test_client.post(base_url, json=new_submenu)

    submenu_id = response.json()["id"]
    submenu_id = submenu_id[:-5] + "1" * 5
    url = app.url_path_for(
        "delete_submenu",
        menu_id=menu_id,
        submenu_id=submenu_id,
    )

    response = await test_client.delete(url)
    assert response.status_code == 404


async def test_patch_submenu(test_client: AsyncClient, menu_id):
    base_url = app.url_path_for("create_submenu", menu_id=menu_id)
    new_submenu = {
        "title": "My submenu 1",
        "description": "My submenu description 1",
    }
    response = await test_client.post(base_url, json=new_submenu)

    submenu_id = response.json()["id"]

    url = app.url_path_for(
        "update_submenu",
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
    updated_submenu = {
        "title": "updated My submenu 1",
        "description": "updated My submenu description 1",
    }
    response = await test_client.patch(url, json=updated_submenu)
    expected_answer = {
        "title": "updated My submenu 1",
        "description": "updated My submenu description 1",
        "id": submenu_id,
    }
    response_dict = response.json()
    assert response.status_code == 200
    assert expected_answer["title"] == response_dict["title"]
    assert expected_answer["description"] == response_dict["description"]
    assert expected_answer["id"] == response_dict["id"]


async def test_patch_submenu_invalid(test_client: AsyncClient, menu_id):
    base_url = app.url_path_for("create_submenu", menu_id=menu_id)
    new_submenu = {
        "title": "My submenu 1",
        "description": "My submenu description 1",
    }
    response = await test_client.post(base_url, json=new_submenu)

    submenu_id = response.json()["id"]
    submenu_id = submenu_id[:-5] + "1" * 5
    url = app.url_path_for(
        "update_submenu",
        menu_id=menu_id,
        submenu_id=submenu_id,
    )

    updated_submenu = {
        "title": "updated My submenu 1",
        "description": "updated My submenu description 1",
    }
    response = await test_client.patch(url, json=updated_submenu)
    assert response.status_code == 404

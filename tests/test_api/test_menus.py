from uuid import UUID

import pytest
from httpx import AsyncClient

from main import app

base_url = app.url_path_for("create_menu")


@pytest.mark.anyio
async def test_empty_menus(test_client: AsyncClient, test_db):
    response = await test_client.get(base_url)
    assert response.status_code == 200
    expected_answer: list = []
    assert expected_answer == response.json()


@pytest.mark.anyio
async def test_menu_create(test_client: AsyncClient, test_db):
    new_menu = {
        "title": "My menu 1",
        "description": "My menu description 1",
    }
    response = await test_client.post(base_url, json=new_menu)

    assert response.status_code == 201

    expected_answer = {
        "title": "My menu 1",
        "description": "My menu description 1",
    }
    response_dict = response.json()
    assert expected_answer["title"] == response_dict["title"]
    assert expected_answer["description"] == response_dict["description"]
    assert isinstance(UUID(response_dict["id"]), UUID)


@pytest.mark.anyio
async def test_detailed_menu(test_client: AsyncClient, test_db):
    new_menu = {
        "title": "My menu 1",
        "description": "My menu description 1",
    }
    response = await test_client.post(base_url, json=new_menu)

    menu_id = response.json()["id"]
    url = app.url_path_for("get_menu", menu_id=menu_id)

    response = await test_client.get(url)
    expected_answer = {
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0,
        "id": menu_id,
    }
    response_dict = response.json()
    assert response.status_code == 200
    assert expected_answer["title"] == response_dict["title"]
    assert expected_answer["description"] == response_dict["description"]
    assert expected_answer["submenus_count"] == response_dict["submenus_count"]
    assert expected_answer["dishes_count"] == response_dict["dishes_count"]
    assert expected_answer["id"] == response_dict["id"]


@pytest.mark.anyio
async def test_detailed_menu_invalid(test_client: AsyncClient, test_db):
    new_menu = {
        "title": "My menu 1",
        "description": "My menu description 1",
    }
    response = await test_client.post(base_url, json=new_menu)

    menu_id = response.json()["id"]
    menu_id = menu_id[:-5] + "1" * 5
    url = app.url_path_for("get_menu", menu_id=menu_id)

    response = await test_client.get(url)
    assert response.status_code == 404


@pytest.mark.anyio
async def test_delete_menu(test_client: AsyncClient, test_db):
    new_menu = {
        "title": "My menu 1",
        "description": "My menu description 1",
    }
    response = await test_client.post(base_url, json=new_menu)

    menu_id = response.json()["id"]
    url = app.url_path_for("delete_menu", menu_id=menu_id)

    response = await test_client.delete(url)
    expected_answer = {
        "deleted": True,
    }
    assert response.status_code == 200
    assert expected_answer == response.json()


@pytest.mark.anyio
async def test_delete_menu_invalid(test_client: AsyncClient, test_db):
    new_menu = {
        "title": "My menu 1",
        "description": "My menu description 1",
    }
    response = await test_client.post(base_url, json=new_menu)

    menu_id = response.json()["id"]
    menu_id = menu_id[:-5] + "1" * 5
    url = app.url_path_for("delete_menu", menu_id=menu_id)

    response = await test_client.delete(url)
    assert response.status_code == 404


@pytest.mark.anyio
async def test_patch_menu(test_client: AsyncClient, test_db):
    new_menu = {
        "title": "My menu 1",
        "description": "My menu description 1",
    }
    response = await test_client.post(base_url, json=new_menu)

    menu_id = response.json()["id"]

    url = app.url_path_for("update_menu", menu_id=menu_id)
    updated_menu = {
        "title": "updated My menu 1",
        "description": "updated My menu description 1",
    }
    response = await test_client.patch(url, json=updated_menu)
    expected_answer = {
        "title": "updated My menu 1",
        "description": "updated My menu description 1",
        "id": menu_id,
    }
    response_dict = response.json()
    assert response.status_code == 200
    assert expected_answer["title"] == response_dict["title"]
    assert expected_answer["description"] == response_dict["description"]
    assert expected_answer["id"] == response_dict["id"]


@pytest.mark.anyio
async def test_patch_menu_invalid(test_client: AsyncClient, test_db):
    new_menu = {
        "title": "My menu 1",
        "description": "My menu description 1",
    }
    response = await test_client.post(base_url, json=new_menu)

    menu_id = response.json()["id"]
    menu_id = menu_id[:-5] + "1" * 5
    url = app.url_path_for("update_menu", menu_id=menu_id)

    updated_menu = {
        "title": "updated My menu 1",
        "description": "updated My menu description 1",
    }
    response = await test_client.patch(url, json=updated_menu)
    assert response.status_code == 404

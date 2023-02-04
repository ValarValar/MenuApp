import math
from uuid import UUID

import pytest
from httpx import AsyncClient

from main import app

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="function")
async def path_ids(test_client: AsyncClient):
    base_url = app.url_path_for("create_menu")
    new_menu = {
        "title": "My menu 1",
        "description": "My menu description 1",
    }
    response = await test_client.post(base_url, json=new_menu)
    menu_id = response.json()["id"]

    url = app.url_path_for("create_submenu", menu_id=menu_id)
    new_submenu = {
        "title": "My dish 1",
        "description": "My dish description 1",
    }
    response = await test_client.post(url, json=new_submenu)
    submenu_id = response.json()["id"]

    return {"menu_id": menu_id, "submenu_id": submenu_id}


async def test_empty_dishes(test_client: AsyncClient, path_ids):
    base_url = app.url_path_for(
        "list_dish",
        menu_id=path_ids["menu_id"],
        submenu_id=path_ids["submenu_id"],
    )
    response = await test_client.get(base_url)
    assert response.status_code == 200
    expected_answer: list = []
    assert expected_answer == response.json()


async def test_dish_create(test_client: AsyncClient, path_ids):
    base_url = app.url_path_for(
        "create_dish",
        menu_id=path_ids["menu_id"],
        submenu_id=path_ids["submenu_id"],
    )
    price: float = 12.5
    new_dish = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": price,
    }
    response = await test_client.post(base_url, json=new_dish)

    assert response.status_code == 201

    expected_answer = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": price,
    }
    response_dict = response.json()
    assert expected_answer["title"] == response_dict["title"]
    assert expected_answer["description"] == response_dict["description"]
    assert math.isclose(price, float(response_dict["price"]))
    assert isinstance(UUID(response_dict["id"]), UUID)


async def test_detailed_dish(test_client: AsyncClient, path_ids):
    base_url = app.url_path_for(
        "create_dish",
        menu_id=path_ids["menu_id"],
        submenu_id=path_ids["submenu_id"],
    )
    new_dish = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": 12.50,
    }
    response = await test_client.post(base_url, json=new_dish)

    dish_id = response.json()["id"]
    url = app.url_path_for(
        "get_dish",
        menu_id=path_ids["menu_id"],
        submenu_id=path_ids["submenu_id"],
        dish_id=dish_id,
    )

    response = await test_client.get(url)
    expected_answer = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "id": dish_id,
    }
    response_dict = response.json()
    assert response.status_code == 200
    assert expected_answer["title"] == response_dict["title"]
    assert expected_answer["description"] == response_dict["description"]
    assert expected_answer["id"] == response_dict["id"]


async def test_detailed_dish_invalid(test_client: AsyncClient, path_ids):
    base_url = app.url_path_for(
        "create_dish",
        menu_id=path_ids["menu_id"],
        submenu_id=path_ids["submenu_id"],
    )
    new_dish = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": 12.50,
    }
    response = await test_client.post(base_url, json=new_dish)

    dish_id = response.json()["id"]
    dish_id = dish_id[:-5] + "1" * 5
    url = app.url_path_for(
        "get_dish",
        menu_id=path_ids["menu_id"],
        submenu_id=path_ids["submenu_id"],
        dish_id=dish_id,
    )

    response = await test_client.get(url)
    assert response.status_code == 404


async def test_delete_dish(test_client: AsyncClient, path_ids):
    base_url = app.url_path_for(
        "create_dish",
        menu_id=path_ids["menu_id"],
        submenu_id=path_ids["submenu_id"],
    )
    new_dish = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": 12.50,
    }
    response = await test_client.post(base_url, json=new_dish)

    dish_id = response.json()["id"]
    url = app.url_path_for(
        "delete_dish",
        menu_id=path_ids["menu_id"],
        submenu_id=path_ids["submenu_id"],
        dish_id=dish_id,
    )

    response = await test_client.delete(url)
    expected_answer = {
        "deleted": True,
    }
    assert response.status_code == 200
    assert expected_answer == response.json()


async def test_delete_dish_invalid(test_client: AsyncClient, path_ids):
    base_url = app.url_path_for(
        "create_dish",
        menu_id=path_ids["menu_id"],
        submenu_id=path_ids["submenu_id"],
    )
    new_dish = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": 12.50,
    }
    response = await test_client.post(base_url, json=new_dish)

    dish_id = response.json()["id"]
    dish_id = dish_id[:-5] + "1" * 5
    url = app.url_path_for(
        "delete_dish",
        menu_id=path_ids["menu_id"],
        submenu_id=path_ids["submenu_id"],
        dish_id=dish_id,
    )

    response = await test_client.delete(url)
    assert response.status_code == 404


async def test_patch_dish(test_client: AsyncClient, path_ids):
    base_url = app.url_path_for(
        "create_dish",
        menu_id=path_ids["menu_id"],
        submenu_id=path_ids["submenu_id"],
    )
    new_dish = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": 12.50,
    }
    response = await test_client.post(base_url, json=new_dish)

    dish_id = response.json()["id"]

    url = app.url_path_for(
        "update_dish",
        menu_id=path_ids["menu_id"],
        submenu_id=path_ids["submenu_id"],
        dish_id=dish_id,
    )
    updated_dish = {
        "title": "updated My dish 1",
        "description": "updated My dish description 1",
    }
    response = await test_client.patch(url, json=updated_dish)
    expected_answer = {
        "title": "updated My dish 1",
        "description": "updated My dish description 1",
        "id": dish_id,
    }
    response_dict = response.json()
    assert response.status_code == 200
    assert expected_answer["title"] == response_dict["title"]
    assert expected_answer["description"] == response_dict["description"]
    assert expected_answer["id"] == response_dict["id"]


async def test_patch_dish_invalid(test_client: AsyncClient, path_ids):
    base_url = app.url_path_for(
        "create_dish",
        menu_id=path_ids["menu_id"],
        submenu_id=path_ids["submenu_id"],
    )
    new_dish = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": 12.50,
    }
    response = await test_client.post(base_url, json=new_dish)

    dish_id = response.json()["id"]
    dish_id = dish_id[:-5] + "1" * 5
    url = app.url_path_for(
        "update_dish",
        menu_id=path_ids["menu_id"],
        submenu_id=path_ids["submenu_id"],
        dish_id=dish_id,
    )

    updated_dish = {
        "title": "updated My dish 1",
        "description": "updated My dish description 1",
    }
    response = await test_client.patch(url, json=updated_dish)
    assert response.status_code == 404

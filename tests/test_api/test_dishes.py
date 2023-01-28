import math
from uuid import UUID

import pytest
from starlette.testclient import TestClient


class TestDishes:
    @pytest.fixture(scope="class")
    def base_url(self, test_client: TestClient, test_db):
        base_url = "/api/v1/menus/"
        new_menu = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response = test_client.post(base_url, json=new_menu)
        menu_id = response.json()['id']

        url = f"/api/v1/menus/{menu_id}/submenus/"
        new_submenu = {
            "title": "My dish 1",
            "description": "My dish description 1"
        }
        response = test_client.post(url, json=new_submenu)
        submenu_id = response.json()['id']

        return f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/"

    def test_empty_dishes(self, test_client: TestClient, test_db, base_url):
        response = test_client.get(base_url)
        assert response.status_code == 200
        expected_answer = []
        assert expected_answer == response.json()

    def test_dish_create(self, test_client: TestClient, test_db, base_url):
        new_dish = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": 12.50
        }
        response = test_client.post(base_url, json=new_dish)

        assert response.status_code == 201

        expected_answer = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": 12.50
        }
        response_dict = response.json()
        assert expected_answer["title"] == response_dict["title"]
        assert expected_answer["description"] == response_dict["description"]
        assert math.isclose(expected_answer["price"], float(response_dict["price"]))
        assert isinstance(UUID(response_dict["id"]), UUID)

    def test_detailed_dish(self, test_client: TestClient, test_db, base_url):
        new_dish = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": 12.50
        }
        response = test_client.post(base_url, json=new_dish)

        last_uuid = response.json()['id']
        url = base_url + last_uuid

        response = test_client.get(url)
        expected_answer = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "id": last_uuid,
        }
        response_dict = response.json()
        assert response.status_code == 200
        assert expected_answer["title"] == response_dict["title"]
        assert expected_answer["description"] == response_dict["description"]
        assert expected_answer["id"] == response_dict["id"]

    def test_detailed_dish_invalid(self, test_client: TestClient, test_db, base_url):
        new_dish = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": 12.50
        }
        response = test_client.post(base_url, json=new_dish)

        last_uuid = response.json()['id']
        last_uuid = last_uuid[:-5] + '1' * 5
        url = base_url + last_uuid

        response = test_client.get(url)
        assert response.status_code == 404

    def test_delete_dish(self, test_client: TestClient, test_db, base_url):
        new_dish = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": 12.50
        }
        response = test_client.post(base_url, json=new_dish)

        last_uuid = response.json()['id']
        url = base_url + last_uuid

        response = test_client.delete(url)
        expected_answer = {
            "deleted": True
        }
        assert response.status_code == 200
        assert expected_answer == response.json()

    def test_delete_dish_invalid(self, test_client: TestClient, test_db, base_url):
        new_dish = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": 12.50
        }
        response = test_client.post(base_url, json=new_dish)

        last_uuid = response.json()['id']
        last_uuid = last_uuid[:-5] + '1' * 5
        url = base_url + last_uuid

        response = test_client.delete(url)
        assert response.status_code == 404

    def test_patch_dish(self, test_client: TestClient, test_db, base_url):
        new_dish = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": 12.50
        }
        response = test_client.post(base_url, json=new_dish)

        last_uuid = response.json()['id']

        url = base_url + last_uuid
        updated_dish = {
            "title": "updated My dish 1",
            "description": "updated My dish description 1"
        }
        response = test_client.patch(url, json=updated_dish)
        expected_answer = {
            "title": "updated My dish 1",
            "description": "updated My dish description 1",
            "id": last_uuid,
        }
        response_dict = response.json()
        assert response.status_code == 200
        assert expected_answer["title"] == response_dict["title"]
        assert expected_answer["description"] == response_dict["description"]
        assert expected_answer["id"] == response_dict["id"]

    def test_patch_dish_invalid(self, test_client: TestClient, test_db, base_url):
        new_dish = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": 12.50
        }
        response = test_client.post(base_url, json=new_dish)

        last_uuid = response.json()['id']
        last_uuid = last_uuid[:-5] + '1' * 5
        url = base_url + last_uuid

        updated_dish = {
            "title": "updated My dish 1",
            "description": "updated My dish description 1"
        }
        response = test_client.patch(url, json=updated_dish)
        assert response.status_code == 404

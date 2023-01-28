from uuid import UUID

from starlette.testclient import TestClient


class TestMenu:
    base_url = '/api/v1/menus/'

    def test_empty_menus(self, test_client: TestClient, test_db):
        response = test_client.get(self.base_url)
        assert response.status_code == 200
        expected_answer = []
        assert expected_answer == response.json()

    def test_menu_create(self, test_client: TestClient, test_db):
        new_menu = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response = test_client.post(self.base_url, json=new_menu)

        assert response.status_code == 201

        expected_answer = {
            "title": "My menu 1",
            "description": "My menu description 1",
        }
        response_dict = response.json()
        assert expected_answer["title"] == response_dict["title"]
        assert expected_answer["description"] == response_dict["description"]
        assert isinstance(UUID(response_dict["id"]), UUID)

    def test_detailed_menu(self, test_client: TestClient, test_db):
        new_menu = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response = test_client.post(self.base_url, json=new_menu)

        last_uuid = response.json()['id']
        url = self.base_url + last_uuid

        response = test_client.get(url)
        expected_answer = {
            "title": "My menu 1",
            "description": "My menu description 1",
            "submenus_count": 0,
            "dishes_count": 0,
            "id": last_uuid,
        }
        response_dict = response.json()
        assert response.status_code == 200
        assert expected_answer["title"] == response_dict["title"]
        assert expected_answer["description"] == response_dict["description"]
        assert expected_answer["submenus_count"] == response_dict["submenus_count"]
        assert expected_answer["dishes_count"] == response_dict["dishes_count"]
        assert expected_answer["id"] == response_dict["id"]

    def test_detailed_menu_invalid(self, test_client: TestClient, test_db):
        new_menu = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response = test_client.post(self.base_url, json=new_menu)

        last_uuid = response.json()['id']
        last_uuid = last_uuid[:-5] + '1' * 5
        url = self.base_url + last_uuid

        response = test_client.get(url)
        assert response.status_code == 404

    def test_delete_menu(self, test_client: TestClient, test_db):
        new_menu = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response = test_client.post(self.base_url, json=new_menu)

        last_uuid = response.json()['id']
        url = self.base_url + last_uuid

        response = test_client.delete(url)
        expected_answer = {
            "deleted": True
        }
        assert response.status_code == 200
        assert expected_answer == response.json()

    def test_delete_menu_invalid(self, test_client: TestClient, test_db):
        new_menu = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response = test_client.post(self.base_url, json=new_menu)

        last_uuid = response.json()['id']
        last_uuid = last_uuid[:-5] + '1' * 5
        url = self.base_url + last_uuid

        response = test_client.delete(url)
        assert response.status_code == 404

    def test_patch_menu(self, test_client: TestClient, test_db):
        new_menu = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response = test_client.post(self.base_url, json=new_menu)

        last_uuid = response.json()['id']

        url = self.base_url + last_uuid
        updated_menu = {
            "title": "updated My menu 1",
            "description": "updated My menu description 1"
        }
        response = test_client.patch(url, json=updated_menu)
        expected_answer = {
            "title": "updated My menu 1",
            "description": "updated My menu description 1",
            "id": last_uuid,
        }
        response_dict = response.json()
        assert response.status_code == 200
        assert expected_answer["title"] == response_dict["title"]
        assert expected_answer["description"] == response_dict["description"]
        assert expected_answer["id"] == response_dict["id"]

    def test_patch_menu_invalid(self, test_client: TestClient, test_db):
        new_menu = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response = test_client.post(self.base_url, json=new_menu)

        last_uuid = response.json()['id']
        last_uuid = last_uuid[:-5] + '1' * 5
        url = self.base_url + last_uuid

        updated_menu = {
            "title": "updated My menu 1",
            "description": "updated My menu description 1"
        }
        response = test_client.patch(url, json=updated_menu)
        assert response.status_code == 404

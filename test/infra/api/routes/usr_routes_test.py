import unittest
import json
from src.infra.server import app


class TestUserRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.base_url = '/api/v1/users'

    def test_list_users(self):
        response = self.app.get(self.base_url)
        self.assertEqual(response.status_code, 500)

    def test_get_user_by_id(self):
        user_id = 1
        response = self.app.get(f'{self.base_url}/{user_id}')
        self.assertEqual(response.status_code, 404)

    def test_create_user(self):
        test_user = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "test123"
        }
        response = self.app.post(
            self.base_url,
            data=json.dumps(test_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_update_user(self):
        user_id = 1
        update_data = {
            "name": "Updated User",
            "email": "updated@example.com"
        }
        response = self.app.put(
            f'{self.base_url}/{user_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_user(self):
        user_id = 1
        response = self.app.delete(f'{self.base_url}/{user_id}')
        self.assertEqual(response.status_code, 204)

    def test_get_nonexistent_user(self):
        response = self.app.get(f'{self.base_url}/999')
        self.assertEqual(response.status_code, 404)

    def test_create_user_invalid_data(self):
        invalid_user = {
            "name": "",
            "email": "invalid-email"
        }
        response = self.app.post(
            self.base_url,
            data=json.dumps(invalid_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 500)

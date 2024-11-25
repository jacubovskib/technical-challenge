import json
from typing import List
from unittest import TestCase
from src.infra.server import app
import random

from src.infra.persistence.entities import UserEntity
from src.infra.db.settings import DBConnectionHandler

class TestUserRoutes(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.base_url = '/api/v1/users'

    def tearDown(self):
        with DBConnectionHandler() as db:
            db.session.query(UserEntity).delete()
            db.session.commit()

    def test_given_three_users_when_list_users_should_return_paginated_response(self):
        # Given
        expected_current_page = 1
        expected_total_items = 3
        expected_per_page = 10
        self._create_users(quantity=3)

        # When
        uri = self.base_url + "?page=1&per_page=10&sort=name&direction=asc"
        response = self.app.get(uri)
        data = json.loads(response.data.decode('utf-8'))

        # Then
        self.assertEqual(expected_per_page, data['per_page'])
        self.assertEqual(expected_current_page, data['current_page'])
        self.assertEqual(expected_total_items, data['total'])
        self.assertEqual(response.status_code, 206)

    def test_given_existing_user_when_get_by_id_should_return_user_data(self):
        # Given
        user_created = self._create_users()
        expected_id = user_created.get('id')
        expected_name = user_created.get('name')
        expected_email = user_created.get('email')

        # When
        response = self.app.get(f'{self.base_url}/{expected_id}')
        data = json.loads(response.data.decode('utf-8'))

        # Then
        self.assertEqual(expected_id, data['id'])
        self.assertEqual(expected_name, data['name'])
        self.assertEqual(expected_email, data['email'])
        self.assertEqual(response.status_code, 200)

    def test_given_valid_user_data_when_create_user_should_return_created_user(self):
        # Given
        test_user = {
            "name": f"Test {random.randint(1000, 9999)}",
            "email": f"test{random.randint(1000, 9999)}@email.com"
        }
        expected_name = test_user.get('name')
        expected_email = test_user.get('email')

        # When
        response = self.app.post(
            self.base_url,
            data=json.dumps(test_user),
            content_type='application/json'
        )
        data = json.loads(response.data.decode('utf-8'))
        expected_id = data.get('id')

        # Then
        self.assertEqual(response.status_code, 201)
        self.assertEqual(expected_id, data['id'])
        self.assertEqual(expected_name, data['name'])
        self.assertEqual(expected_email, data['email'])

    def test_given_existing_user_when_update_should_return_updated_data(self):
        # Given
        created_user = self._create_users()
        expected_name = f"{created_user.get('name')} Att"
        expected_email = f"{created_user.get('email')}.att@example.com"
        update_data = {
            "name": expected_name,
            "email": expected_email
        }

        # When
        response = self.app.put(
            f'{self.base_url}/{created_user.get("id")}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        data = json.loads(response.data.decode('utf-8'))

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_name, data['name'])
        self.assertEqual(expected_email, data['email'])
        self.assertEqual(created_user.get('id'), data['id'])

    def test_given_existing_user_when_delete_should_return_no_content(self):
        # Given
        created_user = self._create_users()

        # When
        response = self.app.delete(f'{self.base_url}/{created_user.get("id")}')

        # Then
        self.assertEqual(response.status_code, 204)

    def test_given_nonexistent_user_when_get_by_id_should_return_not_found(self):
        # When
        response = self.app.get(f'{self.base_url}/999')

        # Then
        self.assertEqual(response.status_code, 404)

    def test_given_invalid_user_data_when_create_user_should_return_validation_error(self):
        # Given
        expected_error_detail = 'Name cannot be empty,Invalid email format'
        expected_error_title = 'Validation error'
        invalid_user = { "name": "", "email": "invalid-email" }

        # When
        response = self.app.post(
            self.base_url,
            data=json.dumps(invalid_user),
            content_type='application/json'
        )
        data = json.loads(response.data.decode('utf-8'))

        # Then
        self.assertEqual(response.status_code, 422)
        self.assertEqual(expected_error_title, data.get('title'))
        self.assertEqual(expected_error_detail, data.get('details'))

    def _create_users(self, quantity=1) -> List[UserEntity]| dict:
        created_users = []

        if quantity == 1:
            return self._create_user()

        for _ in range(quantity):
            response = self._create_user()
            created_users.append(response)
        return created_users

    def _create_user(self):
        test_user = {
            "name": f"Test {random.randint(1000, 9999)}",
            "email": f"test{random.randint(1000, 9999)}@email.com"
        }
        response = self.app.post(
            self.base_url,
            data=json.dumps(test_user),
            content_type='application/json'
        )
        return json.loads(response.data.decode('utf-8'))

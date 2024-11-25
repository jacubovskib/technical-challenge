import unittest
from unittest.mock import Mock

from src.application.usecase.user.create.create_user_input import CreateUserInput
from src.domain.exceptions import NotFoundException
from src.domain.pagination.pagination import Pagination
from src.infra.api.controller.user.user_controller import UserController
from src.infra.api.presentation.http_types.http_request import HttpRequest


class TestUserController(unittest.TestCase):
    def setUp(self):
        self.use_case = Mock()
        self.controller = UserController(self.use_case)

    def tearDown(self):
        self.use_case.reset_mock()

    def test_given_pagination_params_when_list_users_should_return_paginated_response(self):
        # Given
        http_request = HttpRequest(a_query_params={'page': 1, 'per_page': 10})
        expected_pagination = Pagination.of(items=[], total=0, current_page=1, per_page=10)
        self.use_case.execute.return_value = expected_pagination

        # When
        handler = self.controller.handle('list')
        response = handler(http_request)

        # Then
        self.assertEqual(response.status_code, 206)
        self.assertEqual(response.body, expected_pagination)

    def test_given_user_data_when_create_user_should_return_created_user(self):
        # Given
        expected_name = "John Doe"
        expected_email = "john@example.com"
        http_request = HttpRequest(a_body={'name': expected_name, 'email': expected_email})
        expected_output = {'id': 1, 'name': expected_name, 'email': expected_email}
        self.use_case.execute.return_value = expected_output

        # When
        handler = self.controller.handle('create')
        response = handler(http_request)

        # Then
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.body, expected_output)
        self.use_case.execute.assert_called_once_with(
            CreateUserInput(expected_name, expected_email)
        )

    def test_given_update_data_when_update_existing_user_should_return_updated_user(self):
        # Given
        expected_id = 1
        expected_name = "John Updated"
        expected_email = "john.updated@example.com"
        http_request = HttpRequest(
            a_body={'name': expected_name, 'email': expected_email},
            a_path_params={'id': expected_id}
        )
        expected_output = {'id': expected_id, 'name': expected_name, 'email': expected_email}
        self.use_case.execute.return_value = expected_output

        # When
        handler = self.controller.handle('update')
        response = handler(http_request)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, expected_output)

    def test_given_nonexistent_id_when_update_user_should_raise_not_found(self):
        # Given
        http_request = HttpRequest(
            a_body={'name': 'John Updated', 'email': 'john.updated@example.com'},
            a_path_params={'id': 999}
        )
        self.use_case.execute.return_value = None

        # When/Then
        handler = self.controller.handle('update')
        with self.assertRaises(NotFoundException) as error_context:
            handler(http_request)
        self.assertEqual(str(error_context.exception), "User not found")

    def test_given_valid_id_when_delete_user_should_return_no_content(self):
        # Given
        expected_id = 1
        http_request = HttpRequest(a_path_params={'id': expected_id})
        self.use_case.execute.return_value = True

        # When
        handler = self.controller.handle('delete')
        response = handler(http_request)

        # Then
        self.assertEqual(response.status_code, 204)
        self.use_case.execute.assert_called_once_with(expected_id)

    def test_given_nonexistent_id_when_delete_user_should_return_not_found(self):
        # Given
        http_request = HttpRequest(a_path_params={'id': 999})
        self.use_case.execute.return_value = None

        # When
        handler = self.controller.handle('delete')
        response = handler(http_request)

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.body, "User not found")

    def test_given_valid_id_when_get_user_should_return_user_data(self):
        # Given
        expected_id = 1
        expected_output = {'id': expected_id, 'name': 'John Doe', 'email': 'john@example.com'}
        http_request = HttpRequest(a_path_params={'id': expected_id})
        self.use_case.execute.return_value = expected_output

        # When
        handler = self.controller.handle('get')
        response = handler(http_request)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, expected_output)
        self.use_case.execute.assert_called_once_with(expected_id)

    def test_given_invalid_action_when_handle_request_should_return_bad_request(self):
        # Given
        invalid_action = 'invalid_action'

        # When
        handler = self.controller.handle(invalid_action)
        response = handler(HttpRequest())

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.body, {"error": "Invalid action"})

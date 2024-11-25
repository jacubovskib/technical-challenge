import unittest
from unittest.mock import Mock

from src.application.usecase.user.retrive.list.list_user_usecase import ListUserUseCase
from src.domain.pagination.pagination import Pagination
from src.domain.pagination.search_query import SearchQuery
from src.domain.exceptions.types.server_error import ServerError
from src.domain.user.user import User

class TestListUserUseCase(unittest.TestCase):
    def setUp(self):
        self.gateway = Mock()
        self.use_case = ListUserUseCase(self.gateway)
        self.search_query = SearchQuery.of(
            page=1,
            per_page=10,
            sort="name",
            direction="asc"
        )

    def tearDown(self):
        self.gateway.reset_mock()

    def test_given_valid_search_query_when_execute_should_return_user_list(self):
        # Given
        expected_users = [
            User(1, "John Doe", "john@example.com"),
            User(2, "Mary Doe", "mary@example.com"),
            User(3, "Elba Doe", "elba@example.com"),
        ]
        expected_pagination = Pagination(
            current_page=1,
            per_page=10,
            total=3,
            items=expected_users
        )
        self.gateway.list_all_users.return_value = expected_pagination

        # When
        result = self.use_case.execute(self.search_query)

        # Then
        self.assertEqual(result, expected_pagination)
        self.assertEqual(result.current_page, 1)
        self.assertEqual(result.per_page, 10)
        self.assertEqual(result.total, 3)
        self.assertEqual(len(result.items), 3)
        self.assertIsInstance(result.items[0], User)
        self.gateway.list_all_users.assert_called_once_with(self.search_query)

    def test_given_valid_search_query_when_execute_should_return_empty_list(self):
        # Given
        expected_pagination = Pagination(
            current_page=1,
            per_page=10,
            total=0,
            items=[]
        )
        self.gateway.list_all_users.return_value = expected_pagination

        # When
        result = self.use_case.execute(self.search_query)

        # Then
        self.assertEqual(result, expected_pagination)
        self.assertEqual(result.current_page, 1)
        self.assertEqual(result.per_page, 10)
        self.assertEqual(result.total, 0)
        self.assertEqual(len(result.items), 0)
        self.gateway.list_all_users.assert_called_once_with(self.search_query)

    def test_given_valid_search_query_when_execute_should_raise_server_error(self):
        # Given
        error_message = "Internal Server Error"
        self.gateway.list_all_users.side_effect = ServerError(error_message)

        # When/Then
        with self.assertRaises(ServerError):
            self.use_case.execute(self.search_query)

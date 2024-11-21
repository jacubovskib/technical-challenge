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

    def test_given_valid_search_query_when_call_execute_then_return_users(self):
        # Arrange
        expected_total = 3
        expected_per_page = 10
        expected_current_page = 1

        expected_items = [
            User(1, "John Doe", "john@example.com"),
            User(2, "Mary Doe", "mary@example.com"),
            User(3, "Elba Doe", "elba@example.com"),
        ]

        expected_pagination = Pagination(
            current_page=expected_current_page,
            per_page=expected_per_page,
            total=expected_total,
            items=expected_items
        )

        self.gateway.list_all_users.return_value = expected_pagination

        # Act
        result = self.use_case.execute(self.search_query)

        # Assert
        self.assertEqual(result, expected_pagination)
        self.assertEqual(result.current_page, expected_current_page)
        self.assertEqual(result.per_page, expected_per_page)
        self.assertEqual(result.total, expected_total)
        self.assertEqual(len(result.items), expected_total)
        self.assertIsInstance(result.items[0], User)
        self.gateway.list_all_users.assert_called_once_with(self.search_query)

    def test_given_valid_search_query_when_call_execute_then_return_empty_list(self):
        # Arrange
        expected_total = 0
        expected_per_page = 10
        expected_current_page = 1

        expected_pagination = Pagination(
            current_page=expected_current_page,
            per_page=expected_per_page,
            total=expected_total,
            items=[]
        )

        self.gateway.list_all_users.return_value = expected_pagination

        # Act
        result = self.use_case.execute(self.search_query)

        # Assert
        self.assertEqual(result, expected_pagination)
        self.assertEqual(result.current_page, expected_current_page)
        self.assertEqual(result.per_page, expected_per_page)
        self.assertEqual(result.total, expected_total)
        self.assertEqual(len(result.items), expected_total)
        self.gateway.list_all_users.assert_called_once_with(self.search_query)

    def test_given_valid_search_query_when_call_execute_then_return_server_error(self):
        # Arrange
        expected_message = "Internal Server Error"
        self.gateway.list_all_users.side_effect = ServerError(expected_message)

        # Act & Assert
        with self.assertRaises(ServerError):
            self.use_case.execute(self.search_query)
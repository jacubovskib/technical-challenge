import unittest
from unittest.mock import Mock

from src.application.usecase.user.retrive.get.find_user_by_id_usecase import FindUserByIdUseCase
from src.domain.user.user import User

class TestFindUserByIdUseCase(unittest.TestCase):
    def setUp(self):
        self.gateway = Mock()
        self.use_case = FindUserByIdUseCase(self.gateway)

    def tearDown(self):
        self.gateway.reset_mock()

    def test_given_valid_user_id_when_execute_should_return_user(self):
        # Given
        user_id = 1
        expected_user = User(
            an_id=user_id,
            a_name="John Doe",
            an_email="john@example.com"
        )
        self.gateway.get_user.return_value = expected_user

        # When
        result = self.use_case.execute(user_id)

        # Then
        self.assertIsNotNone(result)
        self.assertEqual(result.id, user_id)
        self.assertEqual(result.name, "John Doe")
        self.assertEqual(result.email, "john@example.com")
        self.gateway.get_user.assert_called_once_with(user_id)

    def test_given_nonexistent_user_id_when_execute_should_return_none(self):
        # Given
        user_id = 1
        self.gateway.get_user.return_value = None

        # When
        result = self.use_case.execute(user_id)

        # Then
        self.assertIsNone(result)
        self.gateway.get_user.assert_called_once_with(user_id)

    def test_given_valid_user_id_when_execute_should_raise_server_error(self):
        # Given
        user_id = 1
        error_message = "Internal Server Error"
        self.gateway.get_user.side_effect = Exception(error_message)

        # When/Then
        with self.assertRaises(Exception) as context:
            self.use_case.execute(user_id)

        self.assertEqual(str(context.exception), error_message)
        self.gateway.get_user.assert_called_once_with(user_id)

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

    def test_given_valid_id_when_call_execute_then_return_user(self):
        # Arrange
        expected_id = 1
        expected_name = "John Doe"
        expected_email = "john@example.com"

        a_user = User(
            an_id=expected_id,
            a_name=expected_name,
            an_email=expected_email
        )

        self.gateway.get_user.return_value = a_user

        # Act
        result = self.use_case.execute(expected_id)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.id, expected_id)
        self.assertEqual(result.name, expected_name)
        self.assertEqual(result.email, expected_email)
        self.gateway.get_user.assert_called_once_with(expected_id)

    def test_given_valid_id_when_call_execute_then_return_none(self):
        # Arrange
        user_id = 1
        self.gateway.get_user.return_value = None

        # Act
        result = self.use_case.execute(user_id)

        # Assert
        self.assertIsNone(result)
        self.gateway.get_user.assert_called_once_with(user_id)

    def test_given_valid_id_when_call_execute_then_return_server_error(self):
        # Arrange
        user_id = 1
        expected_message = "Internal Server Error"
        self.gateway.get_user.side_effect = Exception(expected_message)

        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.use_case.execute(user_id)

        self.assertEqual(str(context.exception), expected_message)
        self.gateway.get_user.assert_called_once_with(user_id)
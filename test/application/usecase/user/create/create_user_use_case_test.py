import unittest
from unittest.mock import Mock, patch

from src.application.usecase.user.create.create_user_input import CreateUserInput
from src.application.usecase.user.create.create_user_usecase import CreateUserUseCase
from src.domain.exceptions.types.server_error import ServerError
from src.domain.exceptions.types.validation_exception import ValidationException
from src.domain.user.user import User


class TestCreateUserUseCase(unittest.TestCase):
    def setUp(self):
        self.gateway = Mock()
        self.use_case = CreateUserUseCase(self.gateway)

    def tearDown(self):
        self.gateway.reset_mock()

    def test_given_valid_command_when_calls_create_user_should_return_user(self):
        # Arrange
        expected_name = "John Doe"
        expected_email = "john@example.com"
        command = CreateUserInput(name=expected_name, email=expected_email)

        expected_user = User(a_name=expected_name, an_email=expected_email)
        self.gateway.insert_usr.return_value = expected_user

        # Act
        result = self.use_case.execute(command)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.name, expected_name)
        self.assertEqual(result.email, expected_email)
        self.gateway.insert_usr.assert_called_once_with(expected_user)

    def test_given_invalid_name_when_calls_create_user_should_return_validation_error(self):
        # Arrange
        expected_error_message = "Name cannot be empty"
        command = CreateUserInput(name="", email="john@example.com")

        # Act & Assert
        with self.assertRaises(ValidationException) as error_context:
            self.use_case.execute(command)

        self.assertEqual(str(error_context.exception), expected_error_message)
        self.gateway.insert_usr.assert_not_called()

    def test_given_invalid_email_when_calls_create_user_should_return_validation_error(self):
        # Arrange
        expected_error_message = "Invalid email format"
        command = CreateUserInput(name="John Doe", email="invalid@email")

        # Act & Assert
        with self.assertRaises(ValidationException) as error_context:
            self.use_case.execute(command)

        self.assertEqual(str(error_context.exception), expected_error_message)
        self.gateway.insert_usr.assert_not_called()

    def test_given_valid_command_when_gateway_fails_should_return_error(self):
        # Arrange
        expected_error_message = "Internal Server Error"
        command = CreateUserInput(name="John Doe", email="john@example.com")

        expected_user = User(a_name="John Doe", an_email="john@example.com")
        self.gateway.insert_usr.side_effect = ServerError(expected_error_message)

        # Act & Assert
        with self.assertRaises(ServerError) as error_context:
            self.use_case.execute(command)

        self.assertEqual(str(error_context.exception), expected_error_message)
        self.gateway.insert_usr.assert_called_once_with(expected_user)

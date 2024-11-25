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

    def test_given_valid_input_when_create_user_should_return_user_successfully(self):
        # Given
        expected_name = "John Doe"
        expected_email = "john@example.com"
        input_command = CreateUserInput(name=expected_name, email=expected_email)
        expected_user = User(a_name=expected_name, an_email=expected_email)
        self.gateway.insert_usr.return_value = expected_user

        # When
        result = self.use_case.execute(input_command)

        # Then
        self.assertIsNotNone(result)
        self.assertEqual(result.name, expected_name)
        self.assertEqual(result.email, expected_email)
        self.gateway.insert_usr.assert_called_once_with(expected_user)

    def test_given_empty_name_when_create_user_should_raise_validation_error(self):
        # Given
        expected_error_message = "Name cannot be empty"
        input_command = CreateUserInput(name="", email="john@example.com")

        # When/Then
        with self.assertRaises(ValidationException) as error_context:
            self.use_case.execute(input_command)

        self.assertEqual(str(error_context.exception), expected_error_message)
        self.gateway.insert_usr.assert_not_called()

    def test_given_invalid_email_when_create_user_should_raise_validation_error(self):
        # Given
        expected_error_message = "Invalid email format"
        input_command = CreateUserInput(name="John Doe", email="invalid@email")

        # When/Then
        with self.assertRaises(ValidationException) as error_context:
            self.use_case.execute(input_command)

        self.assertEqual(str(error_context.exception), expected_error_message)
        self.gateway.insert_usr.assert_not_called()

    def test_given_valid_input_when_gateway_fails_should_raise_server_error(self):
        # Given
        expected_error_message = "Internal Server Error"
        input_command = CreateUserInput(name="John Doe", email="john@example.com")
        expected_user = User(a_name="John Doe", an_email="john@example.com")
        self.gateway.insert_usr.side_effect = ServerError(expected_error_message)

        # When/Then
        with self.assertRaises(ServerError) as error_context:
            self.use_case.execute(input_command)

        self.assertEqual(str(error_context.exception), expected_error_message)
        self.gateway.insert_usr.assert_called_once_with(expected_user)

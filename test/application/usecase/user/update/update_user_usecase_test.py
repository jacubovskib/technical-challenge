import unittest
from unittest.mock import Mock

from src.application.usecase.user.update.update_user_usecase import UpdateUserUseCase
from src.application.usecase.user.update.update_user_input import UpdateUserInput
from src.domain.exceptions.types.server_error import ServerError
from src.domain.exceptions.types.validation_exception import ValidationException
from src.domain.user.user import User


class TestUpdateUserUseCase(unittest.TestCase):
    def setUp(self):
        self.gateway = Mock()
        self.use_case = UpdateUserUseCase(self.gateway)

    def tearDown(self):
        self.gateway.reset_mock()

    def test_given_valid_input_when_call_execute_then_update_user(self):
        # Arrange
        expected_id = 1
        expected_name = "New Name"
        expected_email = "new@email.com"

        existing_user = User(an_id=expected_id, a_name="Old Name", an_email="old@email.com")
        self.gateway.get_user.return_value = existing_user

        update_input = UpdateUserInput(
            id=expected_id,
            name=expected_name,
            email=expected_email
        )
        self.gateway.update_user.return_value = update_input

        # Act
        result = self.use_case.execute(update_input)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.id, expected_id)
        self.assertEqual(result.name, expected_name)
        self.assertEqual(result.email, expected_email)
        self.gateway.get_user.assert_called_once_with(expected_id)
        self.gateway.update_user.assert_called_once()

    def test_given_invalid_name_when_call_execute_then_return_validation_error(self):
        # Arrange
        expected_id = 1
        invalid_name = "invalid_name" * 20
        valid_email = "jhon.doe@email.com"
        expected_error_message = "Name must have less than 50 characters"

        existing_user = User(an_id=1, a_name="Old Name", an_email="old@email.com")
        self.gateway.get_user.return_value = existing_user

        update_input = UpdateUserInput(
            id=expected_id,
            name=invalid_name,
            email=valid_email
        )

        # Act & Assert
        with self.assertRaises(ValidationException) as error_context:
            self.use_case.execute(update_input)

        self.assertEqual(str(error_context.exception), expected_error_message)

    def test_given_invalid_email_when_call_execute_then_return_validation_error(self):
        # Arrange
        expected_id = 1
        valid_name = "New Name"
        invalid_email = "invalid-email"
        expected_error_message = "Invalid email format"

        existing_user = User(an_id=expected_id, a_name="Old Name", an_email="old@email.com")
        self.gateway.get_user.return_value = existing_user

        update_input = UpdateUserInput(
            id=expected_id,
            name=valid_name,
            email=invalid_email
        )

        # Act & Assert
        with self.assertRaises(ValidationException) as error_context:
            self.use_case.execute(update_input)

        self.assertEqual(str(error_context.exception), expected_error_message)

    def test_given_nonexistent_user_when_call_execute_then_return_none(self):
        # Arrange
        expected_id = 1
        self.gateway.get_user.return_value = None

        update_input = UpdateUserInput(
            id=expected_id,
            name="Any Name",
            email="any@email.com"
        )

        # Act
        result = self.use_case.execute(update_input)

        # Assert
        self.assertIsNone(result)
        self.gateway.get_user.assert_called_once_with(expected_id)
        self.gateway.update_user.assert_not_called()

    def test_given_valid_input_when_call_execute_then_return_server_error(self):
        # Arrange
        expected_id = 1
        expected_name = "John Doe"
        expected_email = "john@example.com"
        expected_message = "Internal Server Error"

        update_input = UpdateUserInput(
            id=expected_id,
            name=expected_name,
            email=expected_email
        )

        self.gateway.update_user.side_effect = ServerError(expected_message)

        # Act & Assert
        with self.assertRaises(ServerError) as context:
            self.use_case.execute(update_input)

        self.assertEqual(str(context.exception), expected_message)

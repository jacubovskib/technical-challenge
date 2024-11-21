from unittest import TestCase
from src.domain.user.user import User


class TestUser(TestCase):
    def setUp(self):
        self.expected_id = 1
        self.expected_name = "John Doe"
        self.expected_email = "john@example.com"

    def test_given_valid_data_when_create_user_then_return_user(self):
        # Arrange & Act
        user = User(
            an_id=self.expected_id,
            a_name=self.expected_name,
            an_email=self.expected_email
        )

        # Assert
        self.assertEqual(user.id, self.expected_id)
        self.assertEqual(user.name, self.expected_name)
        self.assertEqual(user.email, self.expected_email)

    def test_given_valid_user_when_call_repr_then_return_string_representation(self):
        # Arrange
        user = User(
            an_id=self.expected_id,
            a_name=self.expected_name,
            an_email=self.expected_email
        )
        expected_repr = f"User(id={self.expected_id}, name={self.expected_name}, email={self.expected_email})"

        # Act
        result = repr(user)

        # Assert
        self.assertEqual(result, expected_repr)

    def test_given_valid_user_when_access_properties_then_return_correct_values(self):
        # Arrange & Act
        user = User(
            an_id=self.expected_id,
            a_name=self.expected_name,
            an_email=self.expected_email
        )

        # Assert
        self.assertEqual(user.id, self.expected_id)
        self.assertEqual(user.name, self.expected_name)
        self.assertEqual(user.email, self.expected_email)

    def test_given_valid_user_when_update_then_return_new_user_with_updated_values(self):
        # Arrange
        original_user = User(
            an_id=self.expected_id,
            a_name=self.expected_name,
            an_email=self.expected_email
        )
        new_name = "Jane Doe"
        new_email = "jane@example.com"

        # Act
        updated_user = original_user.update(self.expected_id, new_name, new_email)

        # Assert
        self.assertEqual(updated_user.id, self.expected_id)
        self.assertEqual(updated_user.name, new_name)
        self.assertEqual(updated_user.email, new_email)
        self.assertEqual(original_user.name, self.expected_name)
        self.assertEqual(original_user.email, self.expected_email)
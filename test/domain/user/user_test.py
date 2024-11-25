from unittest import TestCase
from src.domain.user.user import User


class TestUser(TestCase):
    def setUp(self):
        self.expected_id = 1
        self.expected_name = "John Doe"
        self.expected_email = "john@example.com"

    def test_given_valid_user_data_when_creating_user_should_return_user_with_correct_values(self):
        # Given
        user_id = self.expected_id
        user_name = self.expected_name
        user_email = self.expected_email

        # When
        user = User(an_id=user_id, a_name=user_name, an_email=user_email)

        # Then
        self.assertEqual(user.id, self.expected_id)
        self.assertEqual(user.name, self.expected_name)
        self.assertEqual(user.email, self.expected_email)

    def test_given_valid_user_when_getting_string_representation_should_return_formatted_string(self):
        # Given
        user = User(
            an_id=self.expected_id,
            a_name=self.expected_name,
            an_email=self.expected_email
        )
        expected_repr = f"User(id={self.expected_id}, name={self.expected_name}, email={self.expected_email})"

        # When
        result = repr(user)

        # Then
        self.assertEqual(result, expected_repr)

    def test_given_valid_user_when_accessing_properties_should_return_correct_values(self):
        # Given
        user = User(
            an_id=self.expected_id,
            a_name=self.expected_name,
            an_email=self.expected_email
        )

        # When
        user_id = user.id
        user_name = user.name
        user_email = user.email

        # Then
        self.assertEqual(user_id, self.expected_id)
        self.assertEqual(user_name, self.expected_name)
        self.assertEqual(user_email, self.expected_email)

    def test_given_valid_user_when_updating_properties_should_return_new_user_with_updated_values(self):
        # Given
        original_user = User(
            an_id=self.expected_id,
            a_name=self.expected_name,
            an_email=self.expected_email
        )
        new_name = "Jane Doe"
        new_email = "jane@example.com"

        # When
        updated_user = original_user.update(self.expected_id, new_name, new_email)

        # Then
        self.assertEqual(updated_user.id, self.expected_id)
        self.assertEqual(updated_user.name, new_name)
        self.assertEqual(updated_user.email, new_email)
        self.assertEqual(original_user.name, self.expected_name)
        self.assertEqual(original_user.email, self.expected_email)

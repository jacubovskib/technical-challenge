import unittest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from src.domain.exceptions import IntegrityException
from src.domain.pagination.search_query import SearchQuery
from src.domain.user.user import User
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.persistence.repositories import UsersRepository


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.db_connection_handler = DBConnectionHandler()
        self.connection = self.db_connection_handler.get_engine().connect()
        self.repository = UsersRepository()

    def tearDown(self):
        self.connection.execute(text('DELETE FROM users'))
        self.connection.commit()
        self.connection.close()

    def test_given_valid_user_when_insert_then_create_user(self):
        # Arrange
        test_name = "John Doe"
        test_email = "john.doe@example.com"
        user = User(a_name=test_name, an_email=test_email)
        # Act
        self.repository.insert_usr(user)

        # Assert
        result = self.connection.execute(text('SELECT * from users'))
        users = result.fetchall()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].name, test_name)
        self.assertEqual(users[0].email, test_email)

    def test_given_duplicate_user_when_insert_then_raise_unique_error(self):
        # Arrange
        test_name = "John Doe"
        test_email = "john.doe@example.com"
        user = User(a_name=test_name, an_email=test_email)
        self.repository.insert_usr(user)

        # Act & Assert
        with self.assertRaises(IntegrityException) as context:
            self.repository.insert_usr(user)
        self.assertEqual(
            "['Este email já está cadastrado no sistema', 'Este nome já está cadastrado no sistema']",
            str(context.exception))

    def test_given_none_values_when_insert_then_raise_not_null_error(self):
        # Arrange
        test_name = None
        test_email = None
        user = User(a_name=test_name, an_email=test_email)

        # Act & Assert
        with self.assertRaises(IntegrityError) as context:
            self.repository.insert_usr(user)
        self.assertIn("NOT NULL constraint failed: users.name", str(context.exception))

    def test_given_none_email_when_insert_then_raise_not_null_error(self):
        # Arrange
        test_name = "John Doe"
        test_email = None
        user = User(a_name=test_name, an_email=test_email)

        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.repository.insert_usr(user)
        self.assertIn("NOT NULL constraint failed: users.email", str(context.exception))

    def test_given_valid_max_length_when_insert_then_create_user(self):
        # Arrange
        test_name = "A" * 50
        test_email = "a" * 108 + "@test.com"
        user = User(a_name=test_name, an_email=test_email)

        # Act
        self.repository.insert_usr(user)

        # Assert
        result = self.connection.execute(text('SELECT * from users WHERE email = :email'), {'email': test_email})
        user = result.fetchone()
        self.assertEqual(user.name, test_name)
        self.assertEqual(user.email, test_email)

    def test_given_valid_id_when_get_user_then_return_user(self):
        # Arrange
        test_name = "John Doe"
        test_email = "john.doe@example.com"
        user = User(a_name=test_name, an_email=test_email)

        self.repository.insert_usr(user)

        result = self.connection.execute(text('SELECT id from users WHERE email = :email'), {'email': test_email})
        user_id = result.fetchone().id

        # Act
        user = self.repository.get_user(user_id)

        # Assert
        self.assertEqual(user.name, test_name)
        self.assertEqual(user.email, test_email)
        self.assertEqual(user.id, user_id)

    def test_given_invalid_id_when_get_user_then_return_none(self):
        # Arrange
        non_existent_id = 99999

        # Act
        user = self.repository.get_user(non_existent_id)

        # Assert
        self.assertIsNone(user)

    def test_given_valid_user_when_update_then_update_user(self):
        # Arrange
        initial_name = "John Doe"
        initial_email = "john@example.com"
        updated_name = "John Updated"
        updated_email = "john_updated@example.com"
        user = User(a_name=initial_name, an_email=initial_email)

        self.repository.insert_usr(user)
        result = self.connection.execute(text('SELECT id from users WHERE email = :email'), {'email': initial_email})
        user_id = result.fetchone().id

        # Act
        updated_user = user.update(user_id, updated_name, updated_email)
        self.repository.update_user(updated_user)

        # Assert
        updated_user = self.repository.get_user(user_id)
        self.assertEqual(updated_user.name, updated_name)
        self.assertEqual(updated_user.email, updated_email)

    def test_given_empty_database_when_list_all_then_return_empty_list(self):
        # Act
        search_query = SearchQuery.of(
            page=1,
            per_page=10,
            sort="name",
            direction="asc"
        )
        user_paginated = self.repository.list_all_users(search_query)

        # Assert
        self.assertEqual(user_paginated.total, 0)
        self.assertEqual(user_paginated.per_page, 10)
        self.assertEqual(user_paginated.current_page, 1)
        self.assertEqual(user_paginated.items, [])

    def test_given_users_when_list_all_then_return_user_list(self):
        # Arrange
        test_users = [
            User(a_name="Jane2 Doe", an_email="jane2@example.com"),
            User(a_name="John2 Doe", an_email="john2@example.com"),
        ]
        search_query = SearchQuery.of(
            page=1,
            per_page=10,
            sort="name",
            direction="asc"
        )
        for user in test_users:
            self.repository.insert_usr(user)

        # Act
        user_paginated = self.repository.list_all_users(search_query)

        # Assert
        self.assertEqual(user_paginated.total, 2)
        self.assertEqual(user_paginated.per_page, 10)
        self.assertEqual(user_paginated.current_page, 1)

        for i, user in enumerate(test_users):
            self.assertEqual(user_paginated.items[i]['name'], user.name)
            self.assertEqual(user_paginated.items[i]['email'], user.email)

    def test_given_valid_user_when_delete_then_remove_user(self):
        # Arrange
        test_name = "John Doe"
        test_email = "john@example.com"
        user = User(a_name=test_name, an_email=test_email)
        self.repository.insert_usr(user)
        result = self.connection.execute(text('SELECT id from users WHERE email = :email'), {'email': test_email})
        user_id = result.fetchone().id

        # Act
        self.repository.delete_user(user_id)

        # Assert
        result = self.connection.execute(text('SELECT * FROM users'))
        users = result.fetchall()
        self.assertEqual(len(users), 0)

    def test_given_nonexistent_user_when_delete_then_return_none(self):
        # Arrange
        non_existent_id = 999

        # Act & Assert
        user = self.repository.delete_user(non_existent_id)

        self.assertFalse(user)

    def test_given_multiple_users_when_delete_one_then_maintain_others(self):
        # Arrange
        test_users = [
            User(a_name="John Doe", an_email="john@example.com"),
            User(a_name="Jane Doe", an_email="jane@example.com"),
            User(a_name="Bob Smith", an_email="bob@example.com")
        ]
        search_query = SearchQuery.of(
            page=1,
            per_page=10,
            sort="name",
            direction="asc"
        )
        for user in test_users:
            self.repository.insert_usr(user)

        result = self.connection.execute(text('SELECT id from users WHERE email = :email'), {'email': "jane@example.com"})
        jane_id = result.fetchone().id

        # Act
        self.repository.delete_user(jane_id)

        # Assert
        user_paginated = self.repository.list_all_users(search_query)

        self.assertEqual(user_paginated.total, 2)
        self.assertEqual(user_paginated.per_page, 10)
        self.assertEqual(user_paginated.current_page, 1)
        self.assertTrue(all(user['email'] != "jane@example.com" for user in user_paginated.items))

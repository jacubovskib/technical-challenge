import unittest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from src.domain.exceptions import IntegrityException
from src.domain.pagination.search_query import SearchQuery
from src.domain.user.user import User
from src.infra.config import settings
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

    def test_given_valid_user_when_insert_should_create_user(self):
        # Given
        test_name = "John Doe"
        test_email = "john.doe@example.com"
        user = User(a_name=test_name, an_email=test_email)

        # When
        self.repository.insert_usr(user)

        # Then
        result = self.connection.execute(text('SELECT * from users'))
        users = result.fetchall()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].name, test_name)
        self.assertEqual(users[0].email, test_email)

    def test_given_duplicate_user_when_insert_should_raise_integrity_exception(self):
        # Given
        test_name = "John Doe"
        test_email = "john.doe@example.com"
        user = User(a_name=test_name, an_email=test_email)
        self.repository.insert_usr(user)

        # When/Then
        with self.assertRaises(IntegrityException) as context:
            self.repository.insert_usr(user)
        self.assertEqual(
            "['Este email já está cadastrado no sistema', 'Este nome já está cadastrado no sistema']",
            str(context.exception))

    def test_given_null_values_when_insert_should_raise_not_null_error(self):
        # Given
        test_name = None
        test_email = None
        user = User(a_name=test_name, an_email=test_email)

        # When/Then
        with self.assertRaises(IntegrityError) as context:
            self.repository.insert_usr(user)
        self.assertIn("NOT NULL constraint failed: users.name", str(context.exception))

    def test_given_null_email_when_insert_should_raise_not_null_error(self):
        # Given
        test_name = "John Doe"
        test_email = None
        user = User(a_name=test_name, an_email=test_email)

        # When/Then
        with self.assertRaises(Exception) as context:
            self.repository.insert_usr(user)
        self.assertIn("NOT NULL constraint failed: users.email", str(context.exception))

    def test_given_max_length_values_when_insert_should_create_user(self):
        # Given
        test_name = "A" * 50
        test_email = "a" * 108 + "@test.com"
        user = User(a_name=test_name, an_email=test_email)

        # When
        self.repository.insert_usr(user)

        # Then
        result = self.connection.execute(text('SELECT * from users WHERE email = :email'), {'email': test_email})
        user = result.fetchone()
        self.assertEqual(user.name, test_name)
        self.assertEqual(user.email, test_email)

    def test_given_valid_id_when_get_user_should_return_user(self):
        # Given
        test_name = "John Doe"
        test_email = "john.doe@example.com"
        user = User(a_name=test_name, an_email=test_email)
        self.repository.insert_usr(user)
        result = self.connection.execute(text('SELECT id from users WHERE email = :email'), {'email': test_email})
        user_id = result.fetchone().id

        # When
        user = self.repository.get_user(user_id)

        # Then
        self.assertEqual(user.name, test_name)
        self.assertEqual(user.email, test_email)
        self.assertEqual(user.id, user_id)

    def test_given_invalid_id_when_get_user_should_return_none(self):
        # Given
        non_existent_id = 99999

        # When
        user = self.repository.get_user(non_existent_id)

        # Then
        self.assertIsNone(user)

    def test_given_valid_user_when_update_should_modify_user_data(self):
        # Given
        initial_name = "John Doe"
        initial_email = "john@example.com"
        updated_name = "John Updated"
        updated_email = "john_updated@example.com"
        user = User(a_name=initial_name, an_email=initial_email)
        self.repository.insert_usr(user)
        result = self.connection.execute(text('SELECT id from users WHERE email = :email'), {'email': initial_email})
        user_id = result.fetchone().id

        # When
        updated_user = user.update(user_id, updated_name, updated_email)
        self.repository.update_user(updated_user)

        # Then
        updated_user = self.repository.get_user(user_id)
        self.assertEqual(updated_user.name, updated_name)
        self.assertEqual(updated_user.email, updated_email)

    def test_given_empty_database_when_list_all_should_return_empty_list(self):
        # Given
        search_query = SearchQuery.of(
            page=1,
            per_page=10,
            sort="name",
            direction="asc"
        )

        # When
        user_paginated = self.repository.list_all_users(search_query)

        # Then
        self.assertEqual(user_paginated.total, 0)
        self.assertEqual(user_paginated.per_page, 10)
        self.assertEqual(user_paginated.current_page, 1)
        self.assertEqual(user_paginated.items, [])

    def test_given_existing_users_when_list_all_should_return_user_list(self):
        # Given
        test_users = [
            User(a_name="Jane2 Doe", an_email="jane2@example.com"),
            User(a_name="John2 Doe", an_email="john2@example.com"),
        ]
        for user in test_users:
            self.repository.insert_usr(user)
        search_query = SearchQuery.of(
            page=1,
            per_page=10,
            sort="name",
            direction="asc"
        )

        # When
        user_paginated = self.repository.list_all_users(search_query)

        # Then
        self.assertEqual(user_paginated.total, 2)
        self.assertEqual(user_paginated.per_page, 10)
        self.assertEqual(user_paginated.current_page, 1)
        for i, user in enumerate(test_users):
            self.assertEqual(user_paginated.items[i]['name'], user.name)
            self.assertEqual(user_paginated.items[i]['email'], user.email)

    def test_given_existing_user_when_delete_should_remove_user(self):
        # Given
        test_name = "John Doe"
        test_email = "john@example.com"
        user = User(a_name=test_name, an_email=test_email)
        self.repository.insert_usr(user)
        result = self.connection.execute(text('SELECT id from users WHERE email = :email'), {'email': test_email})
        user_id = result.fetchone().id

        # When
        self.repository.delete_user(user_id)

        # Then
        result = self.connection.execute(text('SELECT * FROM users'))
        users = result.fetchall()
        self.assertEqual(len(users), 0)

    def test_given_nonexistent_user_when_delete_should_return_false(self):
        # Given
        non_existent_id = 999

        # When
        result = self.repository.delete_user(non_existent_id)

        # Then
        self.assertFalse(result)

    def test_given_multiple_users_when_delete_one_should_maintain_others(self):
        # Given
        test_users = [
            User(a_name="John Doe", an_email="john@example.com"),
            User(a_name="Jane Doe", an_email="jane@example.com"),
            User(a_name="Bob Smith", an_email="bob@example.com")
        ]
        for user in test_users:
            self.repository.insert_usr(user)
        result = self.connection.execute(text('SELECT id from users WHERE email = :email'),
                                         {'email': "jane@example.com"})
        jane_id = result.fetchone().id
        search_query = SearchQuery.of(
            page=1,
            per_page=10,
            sort="name",
            direction="asc"
        )

        # When
        self.repository.delete_user(jane_id)

        # Then
        user_paginated = self.repository.list_all_users(search_query)
        self.assertEqual(user_paginated.total, 2)
        self.assertEqual(user_paginated.per_page, 10)
        self.assertEqual(user_paginated.current_page, 1)
        self.assertTrue(all(user['email'] != "jane@example.com" for user in user_paginated.items))

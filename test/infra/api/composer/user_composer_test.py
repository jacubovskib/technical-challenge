import unittest
from unittest.mock import patch

from src.infra.api.composers.user.user_composer import UserComposer
from src.infra.api.presentation.http_types.http_request import HttpRequest


class TestUserComposer(unittest.TestCase):
    def setUp(self):
        self.composer = UserComposer()

    def test_list_should_return_callable_handler(self):
        # Act
        handler = self.composer.list()

        # Assert
        self.assertTrue(callable(handler))

    def test_get_should_return_callable_handler(self):
        # Act
        handler = self.composer.get()

        # Assert
        self.assertTrue(callable(handler))

    def test_create_should_return_callable_handler(self):
        # Act
        handler = self.composer.create()

        # Assert
        self.assertTrue(callable(handler))

    def test_update_should_return_callable_handler(self):
        # Act
        handler = self.composer.update()

        # Assert
        self.assertTrue(callable(handler))

    def test_delete_should_return_callable_handler(self):
        # Act
        handler = self.composer.delete()

        # Assert
        self.assertTrue(callable(handler))

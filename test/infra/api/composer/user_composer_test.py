import unittest
from unittest.mock import patch

from src.infra.api.composers.user.user_composer import UserComposer
from src.infra.api.presentation.http_types.http_request import HttpRequest


class TestUserComposer(unittest.TestCase):
    def setUp(self):
        self.composer = UserComposer()

    def test_given_list_action_when_compose_should_return_callable_handler(self):
        # When
        handler = self.composer.list()

        # Then
        self.assertTrue(callable(handler))

    def test_given_get_action_when_compose_should_return_callable_handler(self):
        # When
        handler = self.composer.get()

        # Then
        self.assertTrue(callable(handler))

    def test_given_create_action_when_compose_should_return_callable_handler(self):
        # When
        handler = self.composer.create()

        # Then
        self.assertTrue(callable(handler))

    def test_given_update_action_when_compose_should_return_callable_handler(self):
        # When
        handler = self.composer.update()

        # Then
        self.assertTrue(callable(handler))

    def test_given_delete_action_when_compose_should_return_callable_handler(self):
        # When
        handler = self.composer.delete()

        # Then
        self.assertTrue(callable(handler))

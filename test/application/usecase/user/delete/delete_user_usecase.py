import unittest
from unittest.mock import Mock, patch
from src.application.usecase.user.delete.delete_user_usecase import DeleteUserUseCase
from src.domain.user.abs_user_gateway import AbsUsersGateway


class TestDeleteUserUseCase(unittest.TestCase):
    def setUp(self):
        self.gateway = Mock(spec=AbsUsersGateway)
        self.use_case = DeleteUserUseCase(self.gateway)

    def tearDown(self):
        self.gateway.reset_mock()

    def test_given_valid_id_when_delete_user_then_should_be_ok(self):
        # given
        user_id = 1

        # when
        self.gateway.delete_user.return_value = None

        # then
        self.assertIsNone(self.use_case.execute(user_id))
        self.gateway.delete_user.assert_called_once_with(user_id)

    def test_given_invalid_id_when_delete_user_then_should_raise_exception(self):
        # given
        invalid_id = 999
        expected_error_message = "User not found"

        # when
        self.gateway.delete_user.side_effect = RuntimeError(expected_error_message)

        # then
        with self.assertRaises(RuntimeError) as context:
            self.use_case.execute(invalid_id)

        self.assertEqual(str(context.exception), expected_error_message)
        self.gateway.delete_user.assert_called_once_with(invalid_id)

    def test_given_valid_id_when_delete_user_then_should_call_gateway(self):
        # given
        user_id = 1

        # when
        self.gateway.delete_user.return_value = None

        # then
        self.assertIsNone(self.use_case.execute(user_id))
        self.gateway.delete_user.assert_called_once_with(user_id)

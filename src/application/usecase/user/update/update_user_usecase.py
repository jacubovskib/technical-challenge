from typing import List

from src.application.usecase.user.update.abs_update_user_usecase import AbsUpdateUserUseCase
from src.application.usecase.user.update.update_user_input import UpdateUserInput
from src.application.usecase.user.update.update_user_output import UpdateUserOutput
from src.domain.exceptions.types.validation_exception import ValidationException
from src.domain.notification import Notification
from src.domain.user.abs_user_gateway import AbsUsersGateway


class UpdateUserUseCase(AbsUpdateUserUseCase):

    def __init__(self, gateway: AbsUsersGateway):
        self.__gateway = gateway

    def execute(self, an_input: UpdateUserInput) -> UpdateUserOutput | None:
        notification = Notification()

        an_id = an_input.id

        user_to_update = self.__gateway.get_user(an_id)

        if user_to_update is None:
            return None

        user_updated = user_to_update.update(a_name=an_input.name, an_email=an_input.email)

        user_updated.validate(notification)

        if notification.has_errors():
            _errors: List[str] = notification.get_errors()
            raise ValidationException(',\n'.join(_errors))

        self.__gateway.update_user(user_updated)

        return UpdateUserOutput(
            id=user_updated.id,
            name=user_updated.name,
            email=user_updated.email
        )
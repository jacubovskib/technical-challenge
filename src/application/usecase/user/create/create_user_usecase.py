from typing import List

from src.application.usecase.user.create.abs_create_user_usecase import AbsCreateUserUseCase
from src.application.usecase.user.create.create_user_input import CreateUserInput
from src.application.usecase.user.create.create_user_output import CreateUserOutput
from src.domain.exceptions.types.validation_exception import ValidationException
from src.domain.notification import Notification
from src.domain.user.abs_user_gateway import AbsUsersGateway
from src.domain.user.user import User

class CreateUserUseCase(AbsCreateUserUseCase):
    def __init__(self, user_gateway: AbsUsersGateway):
        self.__user_gateway = user_gateway

    def execute(self, input_data: CreateUserInput) -> CreateUserOutput:
        notification = Notification()

        an_user: User = User(
            a_name=input_data.name,
            an_email=input_data.email
        )

        an_user.validate(notification)

        if notification.has_errors():
            _errors: List[str] = notification.get_errors()
            raise ValidationException(','.join(_errors))

        self.__user_gateway.insert_usr(an_user)

        return CreateUserOutput(
            name=an_user.name,
            email=an_user.email
        )

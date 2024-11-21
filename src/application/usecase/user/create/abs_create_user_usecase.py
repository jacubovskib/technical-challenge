from abc import ABC, abstractmethod

from src.application.shared.usecase import UseCase
from src.application.usecase.user.create.create_user_output import CreateUserOutput
from src.application.usecase.user.create.create_user_input import CreateUserInput


class AbsCreateUserUseCase(UseCase[CreateUserInput, CreateUserOutput], ABC):

    @abstractmethod
    def execute(self, input_data: CreateUserInput) -> CreateUserOutput:
        pass
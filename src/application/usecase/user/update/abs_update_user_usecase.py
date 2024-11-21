from abc import ABC, abstractmethod

from src.application.shared.usecase import UseCase
from src.application.usecase.user.update.update_user_input import UpdateUserInput
from src.application.usecase.user.update.update_user_output import UpdateUserOutput


class AbsUpdateUserUseCase(UseCase[UpdateUserInput, UpdateUserOutput], ABC):
    @abstractmethod
    def execute(self, an_input: UpdateUserInput) -> UpdateUserOutput | None:
        raise NotImplementedError
from abc import ABC, abstractmethod


from src.application.shared.usecase import UseCase
from src.application.usecase.user.retrive.get.find_user_by_id_output import FindUserByIdOutput

class AbsFindUserByIdUseCase(UseCase[int, FindUserByIdOutput], ABC):

    @abstractmethod
    def execute(self, input_data: int) -> FindUserByIdOutput | None:
        pass
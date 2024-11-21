from src.application.usecase.user.retrive.get.abs_find_user_by_id_usecase import AbsFindUserByIdUseCase
from src.application.usecase.user.retrive.get.find_user_by_id_output import FindUserByIdOutput
from src.domain.user.abs_user_gateway import AbsUsersGateway

class FindUserByIdUseCase(AbsFindUserByIdUseCase):
    def __init__(self, user_gateway: AbsUsersGateway):
        self.__user_gateway = user_gateway

    def execute(self, an_id: int) -> FindUserByIdOutput | None:
        user = self.__user_gateway.get_user(an_id)

        if not user:
            return None

        return FindUserByIdOutput(user.id, user.name, user.email)
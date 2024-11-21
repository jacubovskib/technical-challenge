from src.application.usecase.user.delete.abs_delete_user_usecase import AbsDeleteUserUseCase
from src.domain.user.abs_user_gateway import AbsUsersGateway



class DeleteUserUseCase(AbsDeleteUserUseCase):
    def __init__(self, gateway: AbsUsersGateway):
        self.__gateway = gateway

    def execute(self, an_id: int) -> bool:
        return self.__gateway.delete_user(an_id)

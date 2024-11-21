from typing import Callable

from src.application.usecase.user.create.create_user_usecase import CreateUserUseCase
from src.application.usecase.user.delete.delete_user_usecase import DeleteUserUseCase
from src.application.usecase.user.retrive.get.find_user_by_id_usecase import FindUserByIdUseCase
from src.application.usecase.user.retrive.list.list_user_usecase import ListUserUseCase
from src.application.usecase.user.update.update_user_usecase import UpdateUserUseCase
from src.infra.api.composers.base_composer import BaseComposer
from src.infra.api.controller.user.user_controller import UserController
from src.infra.api.presentation.http_types.http_request import HttpRequest
from src.infra.api.presentation.http_types.http_response import HttpResponse
from src.infra.db.repositories.users_repository import UsersRepository


class UserComposer(BaseComposer):
    def __init__(self):
        self.__repository = UsersRepository()
        self.__controller = UserController()

    def list(self) -> Callable[[HttpRequest], HttpResponse]:
        self.__controller.use_case = ListUserUseCase(self.__repository)

        return self.__controller.handle('list')

    def get(self) -> Callable[[HttpRequest], HttpResponse]:
        self.__controller.use_case = FindUserByIdUseCase(self.__repository)

        return self.__controller.handle('get')

    def create(self) -> Callable[[HttpRequest], HttpResponse]:
        self.__controller.use_case = CreateUserUseCase(self.__repository)
        return self.__controller.handle('create')

    def update(self) -> Callable[[HttpRequest], HttpResponse]:
        self.__controller.use_case = UpdateUserUseCase(self.__repository)
        return self.__controller.handle('update')


    def delete(self) -> Callable[[HttpRequest], HttpResponse]:
        self.__controller.use_case = DeleteUserUseCase(self.__repository)
        return self.__controller.handle('delete')


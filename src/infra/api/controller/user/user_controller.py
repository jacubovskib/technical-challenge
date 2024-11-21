from typing import Any, Optional, Callable
from src.domain.exceptions import NotFoundException

from src.application.usecase.user.create.create_user_input import CreateUserInput
from src.application.usecase.user.retrive.get.find_user_by_id_output import FindUserByIdOutput
from src.application.usecase.user.retrive.list.list_user_output import ListUserOutput
from src.application.usecase.user.update.update_user_input import UpdateUserInput
from src.application.usecase.user.update.update_user_output import UpdateUserOutput
from src.domain.pagination.pagination import Pagination
from src.domain.pagination.search_query import SearchQuery
from src.infra.api.presentation.http_types.http_request import HttpRequest
from src.infra.api.presentation.http_types.http_response import HttpResponse


class UserController:
    def __init__(self, use_case: Optional[Any] = None):
        self.__use_case = use_case

    @property
    def use_case(self) -> Any:
        return self.__use_case

    @use_case.setter
    def use_case(self, value: Any) -> None:
        self.__use_case = value

    def handle(self, action: str) -> Callable[[HttpRequest], HttpResponse]:
        actions: dict[str, Callable[[HttpRequest], HttpResponse]] = {
            'list': self.__handle_list,
            'create': self.__handle_create,
            'update': self.__handle_update,
            'delete': self.__handle_delete,
            'get': self.__handle_get
        }

        handler = actions.get(action)
        if not handler:
            return lambda _: HttpResponse(a_status_code=400, a_body={"error": "Invalid action"})

        return handler

    def __handle_list(self, http_request: HttpRequest) -> HttpResponse:
        query = SearchQuery.create(http_request)

        output: Pagination[ListUserOutput] = self.__use_case.execute(query)

        return HttpResponse(a_status_code=206, a_body=output)

    def __handle_create(self, http_request: HttpRequest) -> HttpResponse:
        a_name = http_request.body["name"]
        an_email = http_request.body["email"]

        an_input_data = CreateUserInput(a_name, an_email)

        output = self.__use_case.execute(an_input_data)

        return HttpResponse(a_status_code=201, a_body=output)

    def __handle_update(self, http_request: HttpRequest) -> HttpResponse:
        data = UpdateUserInput(
            id=http_request.path_params["id"],
            name=http_request.body["name"],
            email=http_request.body["email"],
        )

        output: UpdateUserOutput | None = self.__use_case.execute(data)

        if output is None:
            raise NotFoundException("User not found")

        return HttpResponse(a_status_code=200, a_body=output)

    def __handle_delete(self, http_request: HttpRequest) -> HttpResponse:
        output = self.__use_case.execute(int(http_request.path_params["id"]))

        if not output:
            return HttpResponse(a_status_code=404, a_body="User not found")

        return HttpResponse(a_status_code=204)

    def __handle_get(self, http_request: HttpRequest) -> HttpResponse:
        an_id: int = http_request.path_params["id"]

        output: FindUserByIdOutput | None = self.__use_case.execute(an_id)

        if output is None:
            return HttpResponse(a_status_code=404, a_body="User not found")

        return HttpResponse(a_status_code=200, a_body=output)

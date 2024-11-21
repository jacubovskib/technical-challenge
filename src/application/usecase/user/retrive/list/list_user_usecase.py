from src.application.usecase.user.retrive.list.abs_list_user_usecase import AbsListUserUseCase
from src.application.usecase.user.retrive.list.list_user_output import ListUserOutput
from src.domain.pagination.pagination import Pagination
from src.domain.pagination.search_query import SearchQuery
from src.domain.user.abs_user_gateway import AbsUsersGateway


class ListUserUseCase(AbsListUserUseCase):
    def __init__(self, user_gateway: AbsUsersGateway):
        self.__user_gateway = user_gateway

    def execute(self, search_query: SearchQuery) -> Pagination[ListUserOutput]:
        response = self.__user_gateway.list_all_users(search_query)

        return response

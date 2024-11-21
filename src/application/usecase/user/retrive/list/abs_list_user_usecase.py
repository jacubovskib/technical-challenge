from abc import ABC, abstractmethod

from src.application.shared.usecase import UseCase
from src.application.usecase.user.retrive.list.list_user_output import ListUserOutput
from src.domain.pagination.pagination import Pagination
from src.domain.pagination.search_query import SearchQuery

class AbsListUserUseCase(UseCase[SearchQuery, Pagination[ListUserOutput]], ABC):

    @abstractmethod
    def execute(self, search_query: SearchQuery) -> Pagination[ListUserOutput]:
        pass
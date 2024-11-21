from abc import ABC, abstractmethod

from src.application.usecase.user.retrive.list.list_user_output import ListUserOutput
from src.domain.pagination.pagination import Pagination
from src.domain.pagination.search_query import SearchQuery
from src.domain.user.user import User

class AbsUsersGateway(ABC):

    @abstractmethod
    def insert_usr(self, an_user: User) -> None: pass

    @abstractmethod
    def get_user(self, an_id: int) -> User: pass

    @abstractmethod
    def list_all_users(self, a_search: SearchQuery) -> Pagination[ListUserOutput]: pass

    @abstractmethod
    def update_user(self, an_user: User) -> None: pass

    @abstractmethod
    def delete_user(self, an_id: int) -> bool: pass

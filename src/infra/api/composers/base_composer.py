from typing import Callable
from abc import ABC, abstractmethod


from src.infra.api.presentation.http_types.http_request import HttpRequest
from src.infra.api.presentation.http_types.http_response import HttpResponse


class BaseComposer(ABC):
    @abstractmethod
    def list(self) ->  Callable[[HttpRequest], HttpResponse]: pass

    @abstractmethod
    def get(self) ->  Callable[[HttpRequest], HttpResponse]: pass

    @abstractmethod
    def create(self) ->  Callable[[HttpRequest], HttpResponse]: pass

    @abstractmethod
    def update(self) ->  Callable[[HttpRequest], HttpResponse]: pass

    @abstractmethod
    def delete(self) ->  Callable[[HttpRequest], HttpResponse]: pass

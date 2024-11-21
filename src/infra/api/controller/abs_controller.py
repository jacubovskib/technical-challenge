from abc import ABC, abstractmethod
from src.infra.api.presentation.http_types.http_request import HttpRequest
from src.infra.api.presentation.http_types.http_response import HttpResponse

class AbsController(ABC):

    @abstractmethod
    def handler(self, http_request: HttpRequest) -> HttpResponse: pass

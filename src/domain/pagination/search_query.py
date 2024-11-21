from dataclasses import dataclass

from src.infra.api.presentation.http_types.http_request import HttpRequest


@dataclass
class SearchQuery:
    page: int
    per_page: int
    terms: str
    sort: str
    direction: str

    @staticmethod
    def create(http_request: HttpRequest) -> 'SearchQuery':
        return SearchQuery(
            page=http_request.query_params.get("page"),
            per_page=http_request.query_params.get("per_page"),
            terms=http_request.query_params.get("terms"),
            sort=http_request.query_params.get("sort"),
            direction=http_request.query_params.get("direction")
        )

    @staticmethod
    def of(page: int, per_page: int, terms:str = None, sort: str = None, direction: str = None) -> 'SearchQuery':
        return SearchQuery(
            page=int(page),
            per_page=int(per_page),
            terms=terms,
            sort=sort,
            direction=direction
        )
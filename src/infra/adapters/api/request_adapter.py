from typing import Callable

from flask import request as FlaskRequest

from src.infra.api.presentation.http_types.http_request import HttpRequest
from src.infra.api.presentation.http_types.http_response import HttpResponse


def request_adapter(request: FlaskRequest, controller: Callable) -> HttpResponse:
    body = None
    if request.data:
        body = request.json


    http_request = HttpRequest(
        a_body=body,
        a_headers=request.headers,
        a_query_params=request.args,
        a_path_params=request.view_args,
        an_url=request.full_path,
    )

    return controller(http_request)
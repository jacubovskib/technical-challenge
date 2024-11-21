from abc import ABC, abstractmethod
from flask import Blueprint, request, jsonify

from src.domain.exceptions.handle_exceptions import HandleException
from src.infra.adapters.api.request_adapter import request_adapter


class BaseRoutes(ABC):
    def __new__(cls):
        instance = super().__new__(cls)
        instance.blueprint = Blueprint(cls.get_blueprint_name(), __name__)
        instance._register_routes()
        return instance

    @abstractmethod
    def _register_routes(self):
        pass

    @abstractmethod
    def get_blueprint_name(cls) -> str:
        pass

    @abstractmethod
    def get_base_path(cls) -> str:
        pass

    def _handle_request(self, composer_method, resource_id=None):
        try:
            if resource_id:
                request.view_args = {'id': resource_id}
            http_response = request_adapter(request, composer_method)
        except Exception as exception:
            http_response = HandleException.handle(exception)

        return jsonify(http_response.body), http_response.status_code

    def get_blueprint(self):
        return self.blueprint

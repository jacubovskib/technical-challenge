from src.infra.api.composers.user.user_composer import UserComposer
from src.infra.api.routes.base_routes import BaseRoutes


class UserRoutes(BaseRoutes):
    def __init__(self):
        self.user_composer = UserComposer()

    @classmethod
    def get_blueprint_name(cls) -> str:
        return 'user_routes'

    @classmethod
    def get_base_path(cls) -> str:
        return '/api/v1/users'

    def _register_routes(self):
        base_path = self.get_base_path()
        self.blueprint.route(f'{base_path}', methods=['GET'])(self.list)
        self.blueprint.route(f'{base_path}/<id>', methods=['GET'])(self.get_by_id)
        self.blueprint.route(f'{base_path}', methods=['POST'])(self.create)
        self.blueprint.route(f'{base_path}/<id>', methods=['PUT'])(self.update)
        self.blueprint.route(f'{base_path}/<id>', methods=['DELETE'])(self.delete)
        return self

    def list(self):
        return self._handle_request(self.user_composer.list())

    def get_by_id(self, id: int):
        return self._handle_request(self.user_composer.get(), id)

    def create(self):
        return self._handle_request(self.user_composer.create())

    def update(self, id: int):
        return self._handle_request(self.user_composer.update(), id)

    def delete(self, id: int):
        return self._handle_request(self.user_composer.delete(), id)

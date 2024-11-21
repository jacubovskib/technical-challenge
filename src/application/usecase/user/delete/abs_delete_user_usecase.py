from abc import ABC, abstractmethod

from src.application.shared.unit_usecase import UnitUseCase


class AbsDeleteUserUseCase(UnitUseCase[int], ABC):
    @abstractmethod
    def execute(self, an_id: int) -> None:
        raise NotImplementedError
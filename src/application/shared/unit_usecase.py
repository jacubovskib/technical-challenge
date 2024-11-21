from abc import ABC, abstractmethod
from typing import TypeVar, Generic

IN = TypeVar('IN')

class UnitUseCase(Generic[IN], ABC):
    @abstractmethod
    def execute(self, input_data: IN) -> None:
        pass

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

IN = TypeVar('IN')
OUT = TypeVar('OUT')

class UseCase(Generic[IN, OUT], ABC):
    @abstractmethod
    def execute(self, input_data: IN) -> OUT:
        pass

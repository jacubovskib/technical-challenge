from abc import ABC, abstractmethod
from typing import TypeVar, Generic

OUT = TypeVar('OUT')

class NullaryUseCase(Generic[OUT], ABC):
    @abstractmethod
    def execute(self) -> OUT:
        pass

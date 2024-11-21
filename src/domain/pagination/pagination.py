from dataclasses import dataclass
from typing import Generic, TypeVar, List


T = TypeVar('T')

@dataclass
class Pagination(Generic[T]):
    current_page: int
    per_page: int
    total: int
    items: List[T]

    @staticmethod
    def of(current_page: int, per_page: int, total: int,items: List[T]):
        return Pagination(current_page, per_page, total, items)
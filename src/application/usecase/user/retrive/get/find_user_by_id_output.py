from dataclasses import dataclass


@dataclass
class FindUserByIdOutput:
    id: int
    name: str
    email: str
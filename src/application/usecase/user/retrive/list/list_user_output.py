from dataclasses import dataclass

@dataclass
class ListUserOutput:
    id: int
    name: str
    email: str
from dataclasses import dataclass

@dataclass
class UpdateUserInput:
    id: int
    name: str
    email: str

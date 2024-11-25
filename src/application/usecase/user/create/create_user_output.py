from dataclasses import dataclass

@dataclass
class CreateUserOutput:
    id: int
    name: str
    email: str
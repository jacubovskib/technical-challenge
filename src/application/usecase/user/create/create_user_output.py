from dataclasses import dataclass

@dataclass
class CreateUserOutput:
    name: str
    email: str
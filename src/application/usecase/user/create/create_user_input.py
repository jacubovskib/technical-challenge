from dataclasses import dataclass

@dataclass
class CreateUserInput:
    name: str
    email: str
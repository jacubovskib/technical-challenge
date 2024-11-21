from dataclasses import dataclass

@dataclass
class UpdateUserOutput:
    id: int
    name: str
    email: str

    def __init__(self, id=None, name=None, email=None):
        self.id = id
        self.name = name
        self.email = email

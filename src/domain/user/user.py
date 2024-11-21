from src.domain.notification import Notification
from src.domain.validators.user_validator import UserValidator

class User:

    def __init__(self, an_id: int=None, a_name: str=None, an_email: str=None) -> None:
        self._id = an_id
        self._name = a_name
        self._email = an_email


    def __repr__(self) -> str:
        return f"User(id={self._id}, name={self._name}, email={self._email})"

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    def update(self, an_id: int = None, a_name: str = None, an_email: str = None) -> 'User':
        return User(
            an_id or self._id,
            a_name or self._name,
            an_email or self._email
        )

    def validate(self, notification: Notification) -> None:
        UserValidator(self, notification).validate()

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (
                self.id == other.id and
                self.name == other.name and
                self.email == other.email
        )
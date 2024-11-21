import re
from src.domain.notification import Notification


class UserValidator:
    EMAIL_PATTERN = r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''

    def __init__(self, user, notification: Notification):
        self._name = user.name
        self._email = user.email
        self._notification = notification

    def validate(self) -> Notification:

        if not self._name:
            self._notification.add_error("Name cannot be empty")
        elif len(self._name) < 3:
            self._notification.add_error("Name must have at least 3 characters")
        elif len(self._name) > 50:
            self._notification.add_error("Name must have less than 50 characters")

        if not self._email:
            self._notification.add_error("Email cannot be empty")
        elif len(self._email) > 120:
            self._notification.add_error("Email must have less than 120 characters")
        elif not re.match(UserValidator.EMAIL_PATTERN, self._email):
            self._notification.add_error("Invalid email format")

        return self._notification

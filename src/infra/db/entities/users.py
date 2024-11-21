from sqlalchemy import Column, Integer, String

from src.domain.user.user import User
from src.infra.db.settings.base import Base


class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

    def to_domain(self) -> 'User':
        return User(
            self.id,
            self.name,
            self.email,
        )

    @staticmethod
    def from_domain(user: User) -> 'UserEntity':
        return UserEntity(
            id=user.id,
            name=user.name,
            email=user.email,
        )

    def __getattribute__(self, __name):
        return super().__getattribute__(__name)


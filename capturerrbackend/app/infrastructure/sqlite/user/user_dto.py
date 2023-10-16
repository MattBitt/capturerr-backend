from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from capturerrbackend.app.infrastructure.sqlite.database import Base

from ....domain.user.user import User
from ....usecase.user import UserReadModel


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class UserDTO(Base):
    """UserDTO is a data transfer object associated with User entity."""

    __tablename__ = "user"

    user_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[int] = mapped_column(index=True, nullable=False)
    updated_at: Mapped[int] = mapped_column(index=True, nullable=False)

    def to_entity(self) -> User:
        return User(
            user_id=self.id,
            user_name=self.user_name,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_read_model(self) -> UserReadModel:
        return UserReadModel(
            id=self.id,
            user_name=self.user_name,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(user: User) -> "UserDTO":
        now = unixtimestamp()
        return UserDTO(
            id=user.user_id,
            user_name=user.user_name,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            created_at=now,
            updated_at=now,
        )

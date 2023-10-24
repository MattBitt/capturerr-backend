from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from capturerrbackend.app.domain.user.user import User
from capturerrbackend.app.infrastructure.sqlite.database import Base
from capturerrbackend.app.usecase.user import UserReadModel

if TYPE_CHECKING:
    from capturerrbackend.app.infrastructure.sqlite import BookDTO, CaptureDTO, TagDTO


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class UserDTO(Base):
    """UserDTO is a data transfer object associated with User entity."""

    __tablename__ = "user"

    user_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=True)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=True)
    books: Mapped[List["BookDTO"]] = relationship(back_populates="user")
    tags: Mapped[List["TagDTO"]] = relationship(back_populates="user")
    captures: Mapped[List["CaptureDTO"]] = relationship(back_populates="user")

    def to_entity(self) -> User:
        return User(
            user_id=self.id,
            user_name=self.user_name,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            hashed_password=self.hashed_password,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )

    def to_read_model(self) -> UserReadModel:
        return UserReadModel(
            id=self.id,
            user_name=self.user_name,
            first_name=self.first_name,
            last_name=self.last_name,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            email=self.email,
            hashed_password=self.hashed_password,
            created_at=str(self.created_at),
            updated_at=str(self.updated_at),
            deleted_at=str(self.deleted_at),
        )

    @staticmethod
    def from_entity(user: User) -> "UserDTO":
        return UserDTO(
            id=user.user_id,
            user_name=user.user_name,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            hashed_password=user.hashed_password,
            created_at=user.created_at,
            updated_at=user.updated_at,
            deleted_at=user.deleted_at,
        )

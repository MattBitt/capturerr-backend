from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from capturerrbackend.app.domain.tag.tag import Tag
from capturerrbackend.app.infrastructure.sqlite.associations import capture_tags
from capturerrbackend.app.infrastructure.sqlite.database import Base
from capturerrbackend.app.usecase.tag import TagReadModel

if TYPE_CHECKING:
    from capturerrbackend.app.infrastructure.sqlite import CaptureDTO, UserDTO


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class TagDTO(Base):
    """TagDTO is a data transfer object associated with Tag entity."""

    __allow_unmapped__ = True
    __tablename__ = "tag"
    text: Mapped[str] = mapped_column(String(17), nullable=False)

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserDTO"] = relationship(back_populates="tags")

    # capture_id: Mapped[str] = mapped_column(String(38))
    # capture_id: Mapped[str] = mapped_column(ForeignKey("capture.id"))
    captures: Mapped[List["CaptureDTO"]] = relationship(
        secondary=capture_tags,
        back_populates="tags",
    )

    def to_entity(self) -> Tag:
        return Tag(
            id=self.id,
            text=self.text,
            user_id=self.user_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_read_model(self) -> TagReadModel:
        return TagReadModel(
            id=self.id,
            text=self.text,
            user_id=self.user_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(tag: Tag) -> "TagDTO":
        now = unixtimestamp()
        return TagDTO(
            id=tag.id,
            text=tag.text,
            user_id=tag.user_id,
            created_at=now,
            updated_at=now,
        )

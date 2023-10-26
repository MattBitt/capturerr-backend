from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from capturerrbackend.app.domain.capture.capture import Capture
from capturerrbackend.app.infrastructure.sqlite.associations import capture_tags
from capturerrbackend.app.infrastructure.sqlite.database import Base
from capturerrbackend.app.usecase.capture import CaptureReadModel

if TYPE_CHECKING:
    from capturerrbackend.app.infrastructure.sqlite import TagDTO, UserDTO


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class CaptureDTO(Base):
    """CaptureDTO is a data transfer object associated with Capture entity."""

    __allow_unmapped__ = True
    __tablename__ = "capture"
    entry: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    entry_type: Mapped[str] = mapped_column(String, nullable=True)

    notes: Mapped[str] = mapped_column(String, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)
    flagged: Mapped[bool] = mapped_column(unique=False, nullable=True)
    priority: Mapped[str] = mapped_column(String, nullable=True)
    happened_at: Mapped[int] = mapped_column(String, nullable=True)
    due_date: Mapped[int] = mapped_column(String, nullable=True)

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserDTO"] = relationship(back_populates="captures")

    tags: Mapped[List["TagDTO"]] = relationship(
        secondary=capture_tags,
        back_populates="captures",
    )

    def to_entity(self) -> Capture:
        return Capture(
            capture_id=self.id,
            entry=self.entry,
            entry_type=self.entry_type,
            notes=self.notes,
            location=self.location,
            flagged=self.flagged,
            priority=self.priority,
            happened_at=self.happened_at,
            due_date=self.due_date,
            user_id=self.user_id,
            # tags=self.tags,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )

    def to_read_model(self) -> CaptureReadModel:
        return CaptureReadModel(
            id=self.id,
            entry=self.entry,
            entry_type=self.entry_type,
            notes=self.notes,
            location=self.location,
            flagged=self.flagged,
            priority=self.priority,
            happened_at=self.happened_at,
            due_date=self.due_date,
            user_id=self.user_id,
            # tags=self.tags,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )

    @staticmethod
    def from_entity(capture: Capture) -> "CaptureDTO":
        now = unixtimestamp()
        return CaptureDTO(
            id=capture.capture_id,
            entry=capture.entry,
            entry_type=capture.entry_type,
            notes=capture.notes,
            location=capture.location,
            flagged=capture.flagged,
            priority=capture.priority,
            happened_at=capture.happened_at,
            due_date=capture.due_date,
            user_id=capture.user_id,
            # tags=capture.tags,
            created_at=now,
            updated_at=now,
            deleted_at=None,
        )

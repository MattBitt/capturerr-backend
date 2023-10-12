from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from capturerrbackend.app.models.capture_tag import capture_tag
from capturerrbackend.core.base.model import Base


class Tag(Base):
    """Tag database model."""

    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432

    captures = relationship(
        "Capture",
        secondary=capture_tag,
        back_populates="tags",
        uselist=True,
        lazy="selectin",
    )
    # user_pk: Mapped[int] = mapped_column(Integer, ForeignKey("users.pk"))

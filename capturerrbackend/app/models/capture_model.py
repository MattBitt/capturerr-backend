from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from capturerrbackend.app.models.capture_tag import capture_tag
from capturerrbackend.core.base.model import Base


class CaptureModel(Base):
    __tablename__ = "captures"

    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uupk: Mapped[UUID] = mapped_column(
        Uuid,
        default=uuid4(),
        nullable=False,
        unique=True,
    )
    text: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432
    notes: Mapped[str] = mapped_column(String(length=200), nullable=True)
    flagged: Mapped[bool] = mapped_column(Boolean, default=True)
    priority: Mapped[str] = mapped_column(String(length=50), nullable=True)
    captured_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=None,
        nullable=True,
    )
    happend_at: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)
    captured_longitude = Column(Float, default=None, nullable=True)
    captured_latitude = Column(Float, default=None, nullable=True)
    due_date = Column(DateTime, default=None, nullable=True)

    tags = relationship(
        "TagModel",
        secondary=capture_tag,
        back_populates="captures",
        uselist=True,
        lazy="selectin",
    )
    user_pk: Mapped[int] = mapped_column(Integer, nullable=True)
    # user_pk: Mapped[UUID] = mapped_column(Uuid, ForeignKey("user.pk"), nullable=True)
    # user: Mapped["User"] = relationship(back_populates="captures")  # type: ignore

    # dazs = relationship(
    #     "DazModel",
    #     backref=backref("capture"),
    #     cascade="all, delete-orphan",
    #     uselist=True,
    #     lazy="selectin",
    # )

    def __repr__(self) -> str:
        return f"Capture(pk={self.pk} name={self.text}"

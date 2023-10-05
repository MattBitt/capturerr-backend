from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import String

from capturerrbackend.db.base import Base
from capturerrbackend.db.models.capture_tag import capture_tag


class CaptureModel(Base):
    __tablename__ = "captures"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    tags = relationship(
        "TagModel",
        secondary=capture_tag,
        back_populates="captures",
        uselist=True,
        lazy="selectin",
    )
    # dazs = relationship(
    #     "DazModel",
    #     backref=backref("capture"),
    #     cascade="all, delete-orphan",
    #     uselist=True,
    #     lazy="selectin",
    # )

    def __repr__(self) -> str:
        return f"Capture(id={self.id} name={self.name}"

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from capturerrbackend.db.base import Base
from capturerrbackend.db.models.capture_tag import capture_tag


class TagModel(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432
    genre = Column(String())
    platform = Column(String())
    price = Column(Integer())

    captures = relationship(
        "CaptureModel",
        secondary=capture_tag,
        back_populates="tags",
        uselist=True,
        lazy="selectin",
    )
    # dazs = relationship(
    #     "DazModel",
    #     backref=backref("tag"),
    #     cascade="all, delete-orphan",
    #     uselist=True,
    #     lazy="selectin",
    # )

    def __repr__(self) -> str:
        return (
            f"Tag(id={self.id}, "
            + f"title={self.title}, "
            + f"platform={self.platform})"
        )

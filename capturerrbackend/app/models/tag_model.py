from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from capturerrbackend.app.models.capture_tag import capture_tag
from capturerrbackend.core.base.model import Base


class TagModel(Base):
    __tablename__ = "tags"

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
            f"Tag(pk={self.pk}, "
            + f"title={self.title}, "
            + f"platform={self.platform})"
        )

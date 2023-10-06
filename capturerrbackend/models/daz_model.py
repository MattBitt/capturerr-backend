from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from capturerrbackend.models.base import Base


class DazModel(Base):
    __tablename__ = "dazs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    comment: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432

    score = Column(Integer())

    bar_id = Column(Integer(), ForeignKey("bars.id"))
    foo_id = Column(Integer(), ForeignKey("foos.id"))

    def __repr__(self) -> str:
        return (
            f"Daz(id={self.id}, " + f"score={self.score}, " + f"bar_id={self.bar_id})"
        )

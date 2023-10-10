from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from capturerrbackend.core.base.model import Base


class DazModel(Base):
    __tablename__ = "dazs"

    comment: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432

    score = Column(Integer())

    bar_pk = Column(Integer(), ForeignKey("bars.pk"))
    foo_pk = Column(Integer(), ForeignKey("foos.pk"))

    def __repr__(self) -> str:
        return (
            f"Daz(pk={self.pk}, " + f"score={self.score}, " + f"bar_pk={self.bar_pk})"
        )

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from capturerrbackend.app.models.bar_foo import bar_foo
from capturerrbackend.core.base.model import Base


class BarModel(Base):
    __tablename__ = "bars"

    title: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432
    genre = Column(String())
    platform = Column(String())
    price = Column(Integer())

    foos = relationship(
        "FooModel",
        secondary=bar_foo,
        back_populates="bars",
        uselist=True,
        lazy="selectin",
    )
    dazs = relationship(
        "DazModel",
        backref=backref("bar"),
        cascade="all, delete-orphan",
        uselist=True,
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return (
            f"Bar(pk={self.pk}, "
            + f"title={self.title}, "
            + f"platform={self.platform})"
        )

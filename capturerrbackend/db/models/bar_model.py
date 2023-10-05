from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy.sql.sqltypes import String

from capturerrbackend.db.base import Base
from capturerrbackend.db.models.bar_foo import bar_foo


class BarModel(Base):
    __tablename__ = "bars"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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
            f"Bar(id={self.id}, "
            + f"title={self.title}, "
            + f"platform={self.platform})"
        )

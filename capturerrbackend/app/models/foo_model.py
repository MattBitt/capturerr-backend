from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from capturerrbackend.app.models.bar_foo import bar_foo
from capturerrbackend.app.models.base import Base


class FooModel(Base):
    __tablename__ = "foos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    bars = relationship(
        "BarModel",
        secondary=bar_foo,
        back_populates="foos",
        uselist=True,
        lazy="selectin",
    )
    dazs = relationship(
        "DazModel",
        backref=backref("foo"),
        cascade="all, delete-orphan",
        uselist=True,
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"Foo(id={self.id} name={self.name}"

from sqlalchemy import String
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from capturerrbackend.app.models.bar_foo import bar_foo
from capturerrbackend.core.base.model import Base


class FooModel(Base):
    __tablename__ = "foos"

    name: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432

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
        return f"Foo(pk={self.pk} name={self.name}"

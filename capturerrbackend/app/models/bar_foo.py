from sqlalchemy import Column, ForeignKey, Table

from capturerrbackend.app.models.base import Base

bar_foo = Table(
    "bar_foos",
    Base.metadata,
    Column("bar_id", ForeignKey("bars.id"), primary_key=True),
    Column("foo_id", ForeignKey("foos.id"), primary_key=True),
    extend_existing=True,
)

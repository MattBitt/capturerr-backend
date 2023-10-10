from sqlalchemy import Column, ForeignKey, Table

from capturerrbackend.core.base.model import Base

bar_foo = Table(
    "bar_foos",
    Base.metadata,
    Column("bar_pk", ForeignKey("bars.pk"), primary_key=True),
    Column("foo_pk", ForeignKey("foos.pk"), primary_key=True),
    extend_existing=True,
)

from sqlalchemy import Column, ForeignKey, Table

from capturerrbackend.core.base.model import Base

capture_tag = Table(
    "capture_tags",
    Base.metadata,
    Column("tag_pk", ForeignKey("tags.pk"), primary_key=True),
    Column("capture_pk", ForeignKey("captures.pk"), primary_key=True),
    extend_existing=True,
)

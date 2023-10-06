from sqlalchemy import Column, ForeignKey, Table

from capturerrbackend.app.models.base import Base

capture_tag = Table(
    "capture_tags",
    Base.metadata,
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
    Column("capture_id", ForeignKey("captures.id"), primary_key=True),
    extend_existing=True,
)

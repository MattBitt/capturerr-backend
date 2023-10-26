from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Table

from capturerrbackend.app.infrastructure.sqlite.database import Base

capture_tags = Table(
    "capture_tags",
    Base.metadata,
    Column("capture_id", ForeignKey("capture.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)

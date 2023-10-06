from sqlalchemy.orm import DeclarativeBase

from capturerrbackend.db.meta import meta
from capturerrbackend.db.mixins import TimestampMixin


class Base(DeclarativeBase, TimestampMixin):
    """Base for all models."""

    metadata = meta

from sqlalchemy.orm import DeclarativeBase

from capturerrbackend.core.db.meta import meta
from capturerrbackend.core.db.mixins import TimestampMixin


class Base(DeclarativeBase, TimestampMixin):
    """Base for all models."""

    metadata = meta

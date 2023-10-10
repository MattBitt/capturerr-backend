"""
_summary_

"""
import sqlalchemy as sa
from sqlalchemy import Boolean, DateTime, Integer, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base for all models."""

    # Ensure all models have the same metadata object.
    metadata = sa.MetaData()
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    is_active = mapped_column(Boolean, default=True)

    created_by: Mapped[int] = mapped_column(Integer, nullable=True)

    updated_by: Mapped[int] = mapped_column(Integer, nullable=True)

    account_pk: Mapped[int] = mapped_column(Integer, nullable=True)

    @declared_attr
    def created_at(self) -> Mapped[DateTime]:
        """
        _summary_

        Returns:
            Mapped[DateTime]: _description_
        """
        return mapped_column(DateTime, default=func.now(), nullable=False)

    @declared_attr
    def updated_at(self) -> Mapped[DateTime]:
        """
        _summary_

        Returns:
            Mapped[DateTime]: _description_
        """
        return mapped_column(
            DateTime,
            default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )

    @declared_attr
    def deleted_at(self) -> Mapped[DateTime]:
        """
        _summary_

        Returns:
            Mapped[DateTime]: _description_
        """
        return mapped_column(DateTime, default=func.now(), nullable=False)

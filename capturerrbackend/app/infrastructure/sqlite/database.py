import sqlalchemy as sa
from sqlalchemy import Boolean, DateTime, Integer, create_engine, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from capturerrbackend.config.configurator import config

engine = create_engine(
    str(config.db_url),
    connect_args={
        "check_same_thread": False,
    },
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


class Base(DeclarativeBase):
    """Base for all models."""

    # Ensure all models have the same metadata object.
    metadata = sa.MetaData()

    id: Mapped[str] = mapped_column(primary_key=True)

    is_active = mapped_column(Boolean, default=True)

    created_by: Mapped[int] = mapped_column(Integer, nullable=True)

    updated_by: Mapped[int] = mapped_column(Integer, nullable=True)

    account_id: Mapped[int] = mapped_column(Integer, nullable=True)

    # @declared_attr
    # def created_at(self) -> Mapped[DateTime]:
    #     """
    #     _summary_

    #     Returns:
    #         Mapped[DateTime]: _description_
    #     """
    #     return mapped_column(DateTime, default=func.now(), nullable=False)

    # @declared_attr
    # def updated_at(self) -> Mapped[DateTime]:
    #     """
    #     _summary_

    #     Returns:
    #         Mapped[DateTime]: _description_
    #     """
    #     return mapped_column(
    #         DateTime,
    #         default=func.now(),
    #         onupdate=func.now(),
    #         nullable=False,
    #     )

    @declared_attr
    def deleted_at(self) -> Mapped[DateTime]:
        """
        _summary_

        Returns:
            Mapped[DateTime]: _description_
        """
        return mapped_column(DateTime, default=func.now(), nullable=False)

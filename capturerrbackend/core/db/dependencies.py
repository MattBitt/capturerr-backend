from collections.abc import AsyncGenerator
from loguru import logger
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import Iterator
from capturerrbackend.app.settings import settings


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    logger.debug("Creating database session from core.db.dependencies.py")
    engine = create_async_engine(str(settings.db_url), echo=settings.db_echo)
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()
            raise


def get_sync_session():  #  -> SessionLocal[Session, None]:
    db_url = "sqlite:///mydata.db"
    engine = create_engine(str(db_url), echo=settings.db_echo)
    factory = sessionmaker(engine)
    with factory() as session:
        try:
            yield session
            session.commit()
        except exc.SQLAlchemyError as error:
            session.rollback()
            logger.error(error)
            raise

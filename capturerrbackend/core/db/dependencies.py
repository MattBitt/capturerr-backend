from collections.abc import AsyncGenerator

from loguru import logger
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

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

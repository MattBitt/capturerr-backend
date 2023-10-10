import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine

from capturerrbackend.app.models import load_all_models
from capturerrbackend.app.settings import settings
from capturerrbackend.core.base.model import Base

logger = logging.getLogger()

load_all_models()


async def migrate_tables() -> None:
    logger.info("Starting to migrate")

    engine = create_async_engine(str(settings.db_url), echo=settings.db_echo)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Done migrating")


if __name__ == "__main__":
    asyncio.run(migrate_tables())

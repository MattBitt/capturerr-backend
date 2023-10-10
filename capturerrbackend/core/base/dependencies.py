from collections.abc import Callable

from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from capturerrbackend.core.db.dependencies import get_db_session

from .model import Base
from .repository import DatabaseRepository


# TODO this probably doesn't belong here
def get_repository(
    model: type[Base],
) -> Callable[[AsyncSession], DatabaseRepository[Base]]:
    def func(
        session: AsyncSession = Depends(get_db_session),
    ) -> DatabaseRepository[Base]:
        return DatabaseRepository(model, session)

    logger.debug("Getting repository from core.base.dependencies.py")
    return func

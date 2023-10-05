from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from capturerrbackend.db.dependencies import get_db_session
from capturerrbackend.db.models.bar_model import BarModel
from capturerrbackend.db.models.foo_model import (  # need this for the db relationship to work
    FooModel,
)


class BarDAO:
    """Class for accessing bar table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_bar_model(self, title: str) -> None:
        """
        Add single bar to session.

        :param title: title of a bar.
        """
        self.session.add(BarModel(title=title))

    async def get_all_bars(self, limit: int, offset: int) -> List[BarModel]:
        """
        Get all bar models with limit/offset pagination.

        :param limit: limit of bars.
        :param offset: offset of bars.
        :return: stream of bars.
        """
        raw_bars = await self.session.execute(
            select(BarModel).limit(limit).offset(offset),
        )

        return list(raw_bars.scalars().fetchall())

    async def filter(
        self,
        title: Optional[str] = None,
    ) -> List[BarModel]:
        """
        Get specific bar model.

        :param title: title of bar instance.
        :return: bar models.
        """
        query = select(BarModel)
        if title:
            query = query.where(BarModel.title == title)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

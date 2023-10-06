from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from capturerrbackend.app.models.daz_model import DazModel
from capturerrbackend.core.db.dependencies import get_db_session


class DazDAO:
    """Class for accessing daz table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_daz_model(self, comment: str) -> None:
        """
        Add single daz to session.

        :param comment: comment of a daz.
        """
        self.session.add(DazModel(comment=comment))

    async def get_all_dazs(self, limit: int, offset: int) -> List[DazModel]:
        """
        Get all daz models with limit/offset pagination.

        :param limit: limit of dazs.
        :param offset: offset of dazs.
        :return: stream of dazs.
        """
        raw_dazs = await self.session.execute(
            select(DazModel).limit(limit).offset(offset),
        )

        return list(raw_dazs.scalars().fetchall())

    async def filter(
        self,
        comment: Optional[str] = None,
    ) -> List[DazModel]:
        """
        Get specific daz model.

        :param comment: comment of daz instance.
        :return: daz models.
        """
        query = select(DazModel)
        if comment:
            query = query.where(DazModel.comment == comment)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

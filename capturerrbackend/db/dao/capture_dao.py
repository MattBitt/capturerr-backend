from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from capturerrbackend.db.dependencies import get_db_session
from capturerrbackend.db.models.capture_model import CaptureModel


class CaptureDAO:
    """Class for accessing capture table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_capture_model(self, name: str) -> None:
        """
        Add single capture to session.

        :param name: name of a capture.
        """
        self.session.add(CaptureModel(name=name))
        await self.session.commit()

    async def get_all_captures(self, limit: int, offset: int) -> List[CaptureModel]:
        """
        Get all capture models with limit/offset pagination.

        :param limit: limit of captures.
        :param offset: offset of captures.
        :return: stream of captures.
        """
        raw_captures = await self.session.execute(
            select(CaptureModel).limit(limit).offset(offset),
        )

        return list(raw_captures.scalars().fetchall())

    async def filter(
        self,
        name: Optional[str] = None,
    ) -> List[CaptureModel]:
        """
        Get specific capture model.

        :param name: name of capture instance.
        :return: capture models.
        """
        query = select(CaptureModel)
        if name:
            query = query.where(CaptureModel.name == name)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def get_by_id(
        self,
        id: int,
    ) -> Optional[CaptureModel]:
        """
        Get specific capture model.

        :param name: name of capture instance.
        :return: capture models.
        """
        query = select(CaptureModel)
        if id:
            query = query.where(CaptureModel.id == id)
        rows = await self.session.execute(query)
        return rows.scalars().first()

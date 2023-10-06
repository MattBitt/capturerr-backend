from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from capturerrbackend.app.models.capture_model import CaptureModel
from capturerrbackend.core.db.dependencies import get_db_session

# type: ignore


class CaptureDAO:
    """Class for accessing capture table."""

    def __init__(
        self,
        session: AsyncSession = Depends(get_db_session),
    ):
        self.session = session

    async def create_capture_model(self, text: str) -> None:  # type: ignore
        """
        Add single capture to session.

        :param text: text of a capture.
        """
        cap = CaptureModel(text=text)
        self.session.add(cap)
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
        text: Optional[str] = None,
    ) -> List[CaptureModel]:
        """
        Get specific capture model.

        :param text: text of capture instance.
        :return: capture models.
        """
        query = select(CaptureModel)
        if text:
            query = query.where(CaptureModel.text == text)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def get_by_id(
        self,
        id: int,
    ) -> Optional[CaptureModel]:
        """
        Get specific capture model.

        :param text: text of capture instance.
        :return: capture models.
        """
        query = select(CaptureModel)
        if id:
            query = query.where(CaptureModel.id == id)
        rows = await self.session.execute(query)
        return rows.scalars().first()

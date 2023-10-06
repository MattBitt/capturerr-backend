from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from capturerrbackend.app.models.tag_model import TagModel
from capturerrbackend.core.db.dependencies import get_db_session


class TagDAO:
    """Class for accessing tag table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_tag_model(self, title: str) -> None:
        """
        Add single tag to session.

        :param title: title of a tag.
        """
        self.session.add(TagModel(title=title))

    async def get_all_tags(self, limit: int, offset: int) -> List[TagModel]:
        """
        Get all tag models with limit/offset pagination.

        :param limit: limit of tags.
        :param offset: offset of tags.
        :return: stream of tags.
        """
        raw_tags = await self.session.execute(
            select(TagModel).limit(limit).offset(offset),
        )

        return list(raw_tags.scalars().fetchall())

    async def filter(
        self,
        title: Optional[str] = None,
    ) -> List[TagModel]:
        """
        Get specific tag model.

        :param title: title of tag instance.
        :return: tag models.
        """
        query = select(TagModel)
        if title:
            query = query.where(TagModel.title == title)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def get_or_create(
        self,
        name: str,
    ) -> TagModel:
        tag = await self.filter(title=name)
        if tag is None or tag == []:
            await self.create_tag_model(title=name)
            tag = await self.filter(title=name)

        return tag[0]
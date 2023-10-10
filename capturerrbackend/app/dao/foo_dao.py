from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from capturerrbackend.app.models.foo_model import FooModel
from capturerrbackend.core.db.dependencies import get_db_session


class FooDAO:
    """Class for accessing foo table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_foo_model(self, name: str) -> None:
        """
        Add single foo to session.

        :param name: name of a foo.
        """
        self.session.add(FooModel(name=name))

    async def get_all_foos(self, limit: int, offset: int) -> List[FooModel]:
        """
        Get all foo models with limit/offset pagination.

        :param limit: limit of foos.
        :param offset: offset of foos.
        :return: stream of foos.
        """
        raw_foos = await self.session.execute(
            select(FooModel).limit(limit).offset(offset),
        )

        return list(raw_foos.scalars().fetchall())

    async def filter(
        self,
        name: Optional[str] = None,
    ) -> List[FooModel]:
        """
        Get specific foo model.

        :param name: name of foo instance.
        :return: foo models.
        """
        query = select(FooModel)
        if name:
            query = query.where(FooModel.name == name)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def get_by_pk(
        self,
        pk: int,
    ) -> Optional[FooModel]:
        """
        Get specific foo model.

        :param name: name of foo instance.
        :return: foo models.
        """
        query = select(FooModel)
        if pk:
            query = query.where(FooModel.pk == pk)
        rows = await self.session.execute(query)
        return rows.scalars().first()

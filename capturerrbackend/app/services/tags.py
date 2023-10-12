from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from capturerrbackend.app.models.tag import Tag
from capturerrbackend.app.repos.tags import TagRepository
from capturerrbackend.app.schemas.tag import TagPayload, TagSchema
from capturerrbackend.core.base.service import BaseService
from capturerrbackend.core.db.dependencies import get_db_session


class TagService(BaseService):
    def __init__(self, db: Annotated[AsyncSession, Depends(get_db_session)]) -> None:
        self.db = db
        self.model = Tag
        self.get_schema = TagSchema
        self.create_schema = TagPayload
        self._repository = TagRepository(
            self.model,
            self.create_schema,
            self.get_schema,
        )

    async def get_tag_by_name(self, name: str) -> TagSchema:
        return await self._repository.get_by_name(name, self.db)

    async def add(self, name: str) -> bool:
        exists = await self._repository.get_by_name(name, self.db)
        if exists:
            return False
        new_tag = self.create_schema(name=name)
        try:
            await self._repository.create(new_tag, self.db)
        except Exception as e:
            print(e)
            return False
        return True

    async def get_all(self) -> list[TagSchema]:
        return await self._repository.list(self.db)

    async def get_or_create(self, name: str) -> TagSchema:
        exists = await self.get_tag_by_name(name)
        if exists:
            return exists
        new_tag = self.create_schema(name=name)
        try:
            tag = await self._repository.create(new_tag, self.db)
        except Exception as e:
            print(e)
            raise e
        return tag

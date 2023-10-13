from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from capturerrbackend.app.models.capture import Capture
from capturerrbackend.app.repos.captures import CaptureRepository
from capturerrbackend.app.schemas.capture import CapturePayload, CaptureSchema
from capturerrbackend.app.schemas.tag import TagPayload, TagSchema
from capturerrbackend.app.services.tags import TagService
from capturerrbackend.core.base.service import BaseService
from capturerrbackend.core.db.dependencies import get_db_session


class CaptureService(BaseService):
    def __init__(self, db: Annotated[AsyncSession, Depends(get_db_session)]) -> None:
        self.tag_service = TagService(db)
        self.db = db
        self.model = Capture
        self.get_schema = CaptureSchema
        self.create_schema = CapturePayload
        self._repository = CaptureRepository(
            self.model,
            self.create_schema,
            self.get_schema,
        )

    async def get_by_text(self, text: str) -> CaptureSchema:
        return await self._repository.get_by_text(text, self.db)

    async def add(self, text: str) -> bool:
        exists = await self.get_by_text(text)
        if exists:
            return False
        new_capture = self.create_schema(text=text)

        try:
            cap = CapturePayload.model_validate(new_capture)
            await self._repository.create(cap, self.db)
        except Exception as e:
            print(e)
            return False
        return True

    async def add_tags(self, cap: CaptureSchema, tags: list[TagSchema]) -> None:
        for tag in tags:
            await self._repository.add_tag(cap, tag, self.db)

    async def get_all(self) -> list[CaptureSchema]:
        return await self._repository.list(self.db)

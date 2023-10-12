from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from capturerrbackend.app.models.capture import Capture
from capturerrbackend.app.schemas.capture import CapturePayload, CaptureSchema
from capturerrbackend.core.base.repository import BaseRepo


class CaptureRepository(BaseRepo[Capture, CapturePayload, CaptureSchema]):
    # def create_with_user(
    #     self, db: AsyncSession, *, obj_in: CapturePayload, user_id: int
    # ) -> Capture:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.orm_model(**obj_in_data, user_id=user_id)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def get_multi_by_user(
    #     self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    # ) -> list[Capture]:
    #     return (
    #         db.query(self.orm_model)
    #         # .filter(Tag.user_id == user_id)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )

    async def get_by_text(
        self,
        text: str,
        db: AsyncSession,
    ) -> Optional[Capture]:
        async with db as session:
            q = select(self.orm_model).filter(Capture.text == text)
            result = await session.execute(q)
            curr = result.scalars()
            return curr.first()

    # async def add_tag(
    #     self,
    #     cap: CaptureSchema,
    #     tag: TagPayload,
    #     db: AsyncSession,
    # ) -> Optional[Capture]:
    #     async with db as session:
    #         q = update(Capture).where(Capture.pk == cap.pk).values(Capture.tags, tag)
    #         try:
    #             result = await session.execute(q)
    #         except Exception as e:
    #             logger.error(f"Error adding tag to capture: {e}")
    #             raise e

    #         curr = result.scalars()
    #         return curr.first()

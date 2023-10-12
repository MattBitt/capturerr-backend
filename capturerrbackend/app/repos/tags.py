from typing import List, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from capturerrbackend.app.models.tag import Tag
from capturerrbackend.app.schemas.tag import TagPayload, TagSchema
from capturerrbackend.core.base.repository import BaseRepo

T1 = TypeVar("T1", bound=Tag)
T2 = TypeVar("T2", bound=TagPayload)
T3 = TypeVar("T3", bound=TagSchema)


class TagRepository(BaseRepo[T1, T2, T3]):
    def create_with_user(self, db: Session, *, obj_in: T2, user_id: int) -> T3:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.orm_model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[T3]:
        return (
            db.query(self.orm_model)
            # .filter(Tag.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def get_by_name(
        self,
        name: str,
        db: AsyncSession,
    ) -> Optional[T3]:
        async with db as session:
            q = select(self.orm_model).filter(self.orm_model.name == name)
            result = await session.execute(q)
            curr = result.scalars()
            return curr.first()

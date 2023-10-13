from typing import Generic, Optional, TypeVar

from loguru import logger
from pydantic import BaseModel
from sqlalchemy import BinaryExpression, ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from .model import Base

Model = TypeVar("Model", bound=Base)


class DatabaseRepository(Generic[Model]):
    """Repository for performing database queries."""

    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def create(self, data: dict) -> Model:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get(self, pk: int) -> Model | None:
        return await self.session.get(self.model, pk)

    async def filter(
        self,
        *expressions: BinaryExpression,  # type: ignore
    ) -> list[Model]:  # type: ignore
        query = select(self.model)
        if expressions:
            query = query.where(*expressions)
        return list(await self.session.scalars(query))


class BaseRepository:
    __entity_type__ = Base

    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_id(self, id_: int) -> ScalarResult[Base]:
        query = select(self.__entity_type__).filter(self.__entity_type__.pk == id_)
        return await self.db.scalars(query)

    async def find_all(self) -> list[ScalarResult[Base]]:
        query = select(self.__entity_type__)
        return list(await self.db.scalars(query))

    async def save(self, entity: Base) -> Base:
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def delete_by_id(self, id_: int) -> None:
        try:
            instance = await self.find_by_id(id_)
            await self.db.delete(instance)
        except Exception as e:
            logger.error(e)


ModelType = TypeVar("ModelType", bound=Base)

GetModel = TypeVar("GetModel", bound=BaseModel)
CreateModel = TypeVar("CreateModel", bound=BaseModel)


class BaseRepo(Generic[ModelType, CreateModel, GetModel]):
    orm_model: ModelType
    get_model: GetModel
    create_model: CreateModel

    def __init__(
        self,
        orm_model: ModelType,
        get_model: GetModel,
        create_model: CreateModel,
        db_pk_field: str = "pk",
    ) -> None:
        self.orm_model = orm_model
        self.get_model = get_model
        self.create_model = create_model
        self.db_pk_field = db_pk_field

    async def get_by_name(self, name: str, db: AsyncSession) -> Optional[GetModel]:
        async with db as session:
            q = select(self.orm_model).filter(self.orm_model.name == name)
            result = await session.execute(q)
            curr = result.scalars()
            return curr.first()

    async def create(self, data: CreateModel, db: AsyncSession) -> GetModel:
        new_instance = self.orm_model(**(data.model_dump()))
        db.add(new_instance)
        await db.commit()
        await db.refresh(new_instance)
        return new_instance

    async def list(self, db: AsyncSession, limit: int = 25) -> list[GetModel]:
        async with db as session:
            q = select(self.orm_model).limit(limit)
            result = await session.execute(q)
            curr = result.scalars()
            return [self.get_model.model_validate(obj) for obj in curr]

    async def get(self, pk_: int, db: AsyncSession) -> GetModel:
        async with db as session:
            where = getattr(self.orm_model, self.db_pk_field) == pk_
            q = select(self.orm_model).where(where)
            result = await session.execute(q)
            curr = result.scalars()
            return self.get_model.model_validate(curr)

    async def delete(self, pk_: int, db: AsyncSession) -> int:
        filter_kwargs = {self.db_pk_field: pk_}
        num_rows = db.query(self.orm_model).filter_by(**filter_kwargs).delete()
        await db.commit()
        return num_rows

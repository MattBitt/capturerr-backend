from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeMeta, Session

GetModel = TypeVar("GetModel", bound=BaseModel)
CreateModel = TypeVar("CreateModel", bound=BaseModel)
ORM = TypeVar("ORM", bound=DeclarativeMeta)


class BaseRepo(Generic[ORM, GetModel, CreateModel]):
    orm_model: ORM
    get_model: type[GetModel]
    create_model: type[CreateModel]

    def __init__(
        self,
        orm_model: ORM,
        get_model: type[GetModel],
        create_model: type[CreateModel],
        db_pk_field: str = "pk",
    ) -> None:
        self.orm_model = orm_model
        self.get_model = get_model
        self.create_model = create_model
        self.db_pk_field = db_pk_field

    def create(self, data: CreateModel, db: Session) -> GetModel:
        new_instance = self.orm_model(**data.dict())
        db.add(new_instance)
        db.commit()
        db.refresh(new_instance)
        return self.get_model.from_orm(new_instance)

    def list(self, db: Session, limit: int = 25) -> list[GetModel]:
        objects = db.query(self.orm_model).limit(limit).all()
        return [self.get_model.from_orm(obj) for obj in objects]

    def get(self, pk_: int, db: Session) -> GetModel:
        where = getattr(self.orm_model, self.db_pk_field) == pk_
        obj = db.query(self.orm_model).filter(where).first()
        return self.get_model.from_orm(obj)

    def delete(self, pk_: int, db: Session) -> int:
        filter_kwargs = {self.db_pk_field: pk_}
        num_rows = db.query(self.orm_model).filter_by(**filter_kwargs).delete()
        db.commit()
        return num_rows

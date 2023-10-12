from pydantic import BaseModel, ConfigDict


class BaseCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseGetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pk: int

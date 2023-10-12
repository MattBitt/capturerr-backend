from pydantic import Field

from capturerrbackend.core.base.schema import BaseCreateSchema, BaseGetSchema


class TagSchema(BaseGetSchema):
    """Tag model."""

    name: str
    # user_pk: Optional[int] = None


class TagPayload(BaseCreateSchema):
    """Tag payload model."""

    name: str = Field(min_length=1, max_length=127)
    # user_pk: Optional[int] = None

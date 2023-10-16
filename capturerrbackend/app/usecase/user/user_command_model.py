from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from capturerrbackend.utils.utils import get_int_timestamp


def now() -> int:
    return get_int_timestamp(datetime.now())


class UserCreateModel(BaseModel):
    """UserCreateModel represents a write model to create a user."""

    user_name: str = Field(
        example="mizzle-bizzle",
    )

    first_name: str = Field(
        example="John",
    )
    last_name: str = Field(example="Doe")
    email: str = Field(example="admin@example.com")
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)


class UserUpdateModel(BaseModel):
    """UserUpdateModel represents a write model to update a user."""

    user_name: str = Field(
        example="mizzle-bizzle",
    )

    first_name: str = Field(
        example="John",
    )
    last_name: str = Field(example="Doe")
    email: str = Field(example="admin@example.com")
    created_at: Optional[int] = Field(example=1136214245000, default_factory=now)

    updated_at: Optional[int] = Field(example=1136214245000, default_factory=now)

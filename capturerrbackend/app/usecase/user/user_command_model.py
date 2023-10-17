from typing import Optional

from pydantic import BaseModel, Field


class UserBaseModel(BaseModel):
    user_name: str = Field(
        example="mizzle-bizzle",
    )

    first_name: str = Field(
        example="John",
    )
    last_name: str = Field(example="Doe")
    email: str = Field(example="admin@example.com")
    is_active: Optional[bool] = Field(example=True, default=True)
    is_superuser: Optional[bool] = Field(example=False, default=False)
    created_at: Optional[int] = Field(example=1136214245000, default=None)
    updated_at: Optional[int] = Field(example=1136214245000, default=None)
    deleted_at: Optional[int] = Field(example=1136214245000, default=None)


class UserCreateModel(UserBaseModel):
    """UserCreateModel represents a write model to create a user."""

    password: str = Field(example="password")


class UserUpdateModel(UserBaseModel):
    """UserUpdateModel represents a write model to update a user."""

    ...

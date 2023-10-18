from typing import Optional

from pydantic import BaseModel, Field


class UserBaseModel(BaseModel):
    user_name: str = Field(
        example="matt",
    )

    first_name: str = Field(
        example="Matt",
    )
    last_name: str = Field(example="Bitt")
    email: str = Field(example="matt@bittfurst.xyz")
    is_superuser: Optional[bool] = Field(example=False, default=False)


class UserCreateModel(UserBaseModel):
    """UserCreateModel represents a write model to create a user."""

    password: str = Field(example="password")


class UserUpdateModel(UserBaseModel):
    """UserUpdateModel represents a write model to update a user."""

    ...

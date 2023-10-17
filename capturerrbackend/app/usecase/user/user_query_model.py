from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from capturerrbackend.app.domain.user.user import User


class UserReadModel(BaseModel):
    """UserReadModel represents data structure as a read model."""

    model_config = ConfigDict(from_attributes=True)
    id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")
    user_name: str = Field(
        example="mizzle-bizzle",
    )
    first_name: str = Field(
        example="John",
    )
    last_name: str = Field(example="Doe")
    email: str = Field(example="admin@example.com")
    is_active: bool = Field(example=True)
    is_superuser: bool = Field(example=False)
    created_at: Optional[str] = Field(example="1136214245000")
    updated_at: Optional[str] = Field(example="1136214245000")
    deleted_at: Optional[str] = Field(example="1136214245000", default=None)
    hashed_password: Optional[str] = Field(example="bjcvljdsaflkrjqewoigfddsaf")

    @staticmethod
    def from_entity(user: User) -> "UserReadModel":
        return UserReadModel(
            id=user.user_id,
            user_name=user.user_name,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            hashed_password=user.hashed_password,
            created_at=str(user.created_at),
            updated_at=str(user.updated_at),
            deleted_at=str(user.deleted_at),
        )


class UserLoginModel(BaseModel):
    """UserLoginModel represents a write model to login a user."""

    user_name: str = Field(
        example="mizzle-bizzle",
    )

    password: str = Field(
        example="password",
    )

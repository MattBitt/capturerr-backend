from typing import cast

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
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)

    @staticmethod
    def from_entity(user: User) -> "UserReadModel":
        return UserReadModel(
            id=user.user_id,
            user_name=user.user_name,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            created_at=cast(int, user.created_at),
            updated_at=cast(int, user.updated_at),
        )

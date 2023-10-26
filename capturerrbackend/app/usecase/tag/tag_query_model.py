from typing import TYPE_CHECKING, List, Optional, cast

from pydantic import BaseModel, ConfigDict, Field

from capturerrbackend.app.domain.tag.tag import Tag
from capturerrbackend.app.usecase.user.user_query_model import UserReadModel

if TYPE_CHECKING:
    from capturerrbackend.app.usecase.capture.capture_query_model import (
        CaptureReadModel,
    )


class TagReadModel(BaseModel):
    """TagReadModel represents data structure as a read model."""

    model_config = ConfigDict(from_attributes=True)
    id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")
    text: str = Field(
        example=["monotone", "nonsense", "POV"],
    )
    user_id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")

    user: Optional[UserReadModel] = Field(default=None)

    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)
    captures: Optional[List["CaptureReadModel"]] = Field(default=None)

    @staticmethod
    def from_entity(tag: Tag) -> "TagReadModel":
        return TagReadModel(
            id=tag.id,
            text=tag.text,
            user_id=tag.user_id,
            created_at=cast(int, tag.created_at),
            updated_at=cast(int, tag.updated_at),
        )

    def __str__(self) -> str:
        return f"TagReadModel(text={self.text}"

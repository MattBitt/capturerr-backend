from typing import List, Optional, cast

from pydantic import BaseModel, ConfigDict, Field

from capturerrbackend.app.domain.capture.capture import Capture
from capturerrbackend.app.usecase.tag.tag_query_model import TagReadModel
from capturerrbackend.app.usecase.user.user_query_model import UserReadModel


class CaptureReadModel(BaseModel):
    """CaptureReadModel represents data structure as a read model."""

    model_config = ConfigDict(from_attributes=True, extra="allow")
    id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")
    entry: str = Field(example="Just ate a cheeseburger.")
    entry_type: str = Field(example="a food journal entry")
    notes: str = Field(
        example="It was delicious!.",
    )
    location: str = Field(example="McDonalds")
    flagged: bool = Field(example=False)
    priority: str = Field(example="low")
    happened_at: int = Field(example=1620000000)
    due_date: int = Field(example=1620000000)
    user_id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)
    user: Optional[UserReadModel] = Field(default=None)
    tags: Optional[List[TagReadModel]] = Field(default=None)

    @staticmethod
    def from_entity(capture: Capture) -> "CaptureReadModel":
        return CaptureReadModel(
            id=capture.capture_id,
            entry=capture.entry,
            entry_type=capture.entry_type,
            notes=capture.notes,
            location=capture.location,
            flagged=capture.flagged,
            priority=capture.priority,
            happened_at=cast(int, capture.happened_at),
            due_date=cast(int, capture.due_date),
            user_id=capture.user_id,
            tags=capture.tags,
            created_at=cast(int, capture.created_at),
            updated_at=cast(int, capture.updated_at),
        )

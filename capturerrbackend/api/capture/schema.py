from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from capturerrbackend.api.tag.schema import TagModelDTO
from capturerrbackend.db.models.users import UserRead  # type: ignore


class CaptureModelDTO(BaseModel):
    """
    DTO for capture models.

    It returned when accessing capture models from the API.
    """

    id: int
    uuid: UUID
    text: str
    notes: Optional[str] = ""
    is_active: Optional[bool] = True
    flagged: Optional[bool] = False
    priority: Optional[str] = ""
    captured_time: Optional[str] = None
    happend_at: Optional[str] = None
    captured_longitude: Optional[float] = None
    captured_latitude: Optional[float] = None
    user: Optional[UserRead] = None
    tags: Optional[list[TagModelDTO]] = None

    model_config = ConfigDict(from_attributes=True)


class CaptureModelInputDTO(BaseModel):
    """DTO for creating new capture model."""

    user_id: Optional[UUID] = None
    user: Optional[UserRead] = None
    text: str
    notes: Optional[str] = ""
    is_active: Optional[bool] = True
    flagged: Optional[bool] = False
    priority: Optional[str] = ""
    captured_time: Optional[str] = None
    happend_at: Optional[str] = None
    captured_longitude: Optional[float] = None
    captured_latitude: Optional[float] = None
    tags: Optional[list[TagModelDTO]] = None

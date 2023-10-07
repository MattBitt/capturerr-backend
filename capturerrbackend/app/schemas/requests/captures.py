from typing import Optional

from pydantic import BaseModel, ConfigDict

from capturerrbackend.app.schemas.requests.tags import TagRequest


class CaptureRequest(BaseModel):
    """DTO for creating new capture model."""

    # TODO not sure if i should be using this model_config
    model_config = ConfigDict(from_attributes=True)
    # user_id: Optional[UUID] = None
    # user: Optional[UserRead] = None
    text: str
    notes: Optional[str] = ""
    is_active: Optional[bool] = True
    flagged: Optional[bool] = False
    priority: Optional[str] = ""
    captured_time: Optional[str] = None
    happend_at: Optional[str] = None
    captured_longitude: Optional[float] = None
    captured_latitude: Optional[float] = None
    tags: Optional[list[TagRequest]] = None

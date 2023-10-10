from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from capturerrbackend.app.schemas.requests.tags import TagRequest


class CaptureResponse(BaseModel):
    """
    DTO for capture models.

    It returned when accessing capture models from the API.
    """

    pk: int
    uupk: UUID
    text: str
    notes: Optional[str] = ""
    is_active: Optional[bool] = True
    flagged: Optional[bool] = False
    priority: Optional[str] = ""
    captured_time: Optional[str] = None
    happend_at: Optional[str] = None
    captured_longitude: Optional[float] = None
    captured_latitude: Optional[float] = None
    # user: Optional[UserRead] = None
    tags: Optional[list[TagRequest]] = None

    model_config = ConfigDict(from_attributes=True)

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .tag import TagPayload, TagSchema


class CaptureSchema(BaseModel):
    """Capture model."""

    model_config = ConfigDict(from_attributes=True)

    pk: int
    text: str
    notes: Optional[str] = ""
    flagged: Optional[bool] = False
    priority: Optional[str] = ""
    captured_time: Optional[datetime]
    happend_at: Optional[datetime]
    captured_longitude: Optional[float] = 0.0
    captured_latitude: Optional[float] = 0.0
    due_date: Optional[datetime]
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None
    is_active: Optional[bool] = True
    created_by: Optional[int]
    updated_by: Optional[int]
    account_pk: Optional[int]
    tags: Optional[list["TagSchema"]] = []


class CapturePayload(BaseModel):
    """Capture payload model."""

    text: str = Field(min_length=1, max_length=200)
    tags: Optional[list[TagPayload]] = []  # Field(min_items=1)

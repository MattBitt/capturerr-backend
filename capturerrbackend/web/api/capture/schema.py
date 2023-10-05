from typing import Optional

from pydantic import BaseModel, ConfigDict

from capturerrbackend.web.api.tag.schema import TagModelDTO


class CaptureModelDTO(BaseModel):
    """
    DTO for capture models.

    It returned when accessing capture models from the API.
    """

    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
    tags: Optional[list[TagModelDTO]] = None


class CaptureModelInputDTO(BaseModel):
    """DTO for creating new capture model."""

    name: str

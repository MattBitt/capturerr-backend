from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from capturerrbackend.web.api.bar.schema import BarModelDTO


class FooModelDTO(BaseModel):
    """
    DTO for foo models.

    It returned when accessing foo models from the API.
    """

    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
    bars: Optional[List[BarModelDTO]] = None


class FooModelInputDTO(BaseModel):
    """DTO for creating new foo model."""

    name: str


# from capturerrbackend.web.api.bar.schema import BarModelDTO

# BarModelDTO.model_rebuild()

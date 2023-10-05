from pydantic import BaseModel, ConfigDict


class TagModelDTO(BaseModel):
    """
    DTO for tag models.

    It returned when accessing tag models from the API.
    """

    id: int
    title: str
    model_config = ConfigDict(from_attributes=True)


class TagModelInputDTO(BaseModel):
    """DTO for creating new tag model."""

    title: str

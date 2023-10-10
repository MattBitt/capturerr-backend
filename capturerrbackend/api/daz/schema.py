from pydantic import BaseModel, ConfigDict


class DazModelDTO(BaseModel):
    """
    DTO for daz models.

    It returned when accessing daz models from the API.
    """

    pk: int
    comment: str
    model_config = ConfigDict(from_attributes=True)


class DazModelInputDTO(BaseModel):
    """DTO for creating new daz model."""

    comment: str

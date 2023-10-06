from pydantic import BaseModel, ConfigDict


class TagResponse(BaseModel):
    """
    DTO for tag models.

    It returned when accessing tag models from the API.
    """

    id: int
    title: str
    model_config = ConfigDict(from_attributes=True)

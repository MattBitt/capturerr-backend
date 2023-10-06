from pydantic import BaseModel, ConfigDict


class BarModelDTO(BaseModel):
    """
    DTO for bar models.

    It returned when accessing bar models from the API.
    """

    id: int
    title: str
    # captures: Optional[List[FooModelDTO]]
    model_config = ConfigDict(from_attributes=True)


class BarModelInputDTO(BaseModel):
    """DTO for creating new bar model."""

    title: str


# from capturerrbackend.api.foo.schema import FooModelDTO

# FooModelDTO.model_rebuild()
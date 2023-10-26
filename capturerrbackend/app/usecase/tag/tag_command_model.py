from pydantic import BaseModel, Field


class TagCreateModel(BaseModel):
    """TagCreateModel represents a write model to create a tag."""

    text: str = Field(
        example="Domain-Driven Design: Tackling Complexity in the Heart of Softwares",
    )
    user_id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")


class TagUpdateModel(BaseModel):
    """TagUpdateModel represents a write model to update a tag."""

    text: str = Field(
        example="monotone",
    )
    user_id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")

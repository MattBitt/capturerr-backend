from pydantic import BaseModel, Field, validator


class BookCreateModel(BaseModel):
    """BookCreateModel represents a write model to create a book."""

    isbn: str = Field(example="978-0321125217")
    title: str = Field(
        example="Domain-Driven Design: Tackling Complexity in the Heart of Softwares",
    )
    page: int = Field(ge=0, example=320)
    user_id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")


class BookUpdateModel(BaseModel):
    """BookUpdateModel represents a write model to update a book."""

    isbn: str = Field(example="978-0321125217")
    title: str = Field(
        example="Domain-Driven Design: Tackling Complexity in the Heart of Softwares",
    )
    page: int = Field(ge=0, example=320)
    user_id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")
    read_page: int = Field(ge=0, example=120)

    @validator("read_page")
    def _validate_read_page(cls, v, values, **kwargs):  # type: ignore
        if "page" in values and v > values["page"]:
            raise ValueError(
                "read_page must be between 0 and {}".format(values["page"]),
            )
        return v

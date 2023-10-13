from typing import cast

from pydantic import BaseModel, Field, ConfigDict

from capturerrbackend.app.domain.book.book import Book


class BookReadModel(BaseModel):
    """BookReadModel represents data structure as a read model."""

    model_config = ConfigDict(from_attributes=True)
    id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")
    isbn: str = Field(example="978-0321125217")
    title: str = Field(
        example="Domain-Driven Design: Tackling Complexity in the Heart of Softwares"
    )
    page: int = Field(ge=0, example=320)
    read_page: int = Field(ge=0, example=120)
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)

    @staticmethod
    def from_entity(book: Book) -> "BookReadModel":
        return BookReadModel(
            id=book.book_id,
            isbn=book.isbn.value,
            title=book.title,
            page=book.page,
            read_page=book.read_page,
            created_at=cast(int, book.created_at),
            updated_at=cast(int, book.updated_at),
        )

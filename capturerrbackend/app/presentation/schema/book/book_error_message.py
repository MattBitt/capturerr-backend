from pydantic import BaseModel, Field

from capturerrbackend.app.domain.book.book_exception import (
    BookIsbnAlreadyExistsError,
    BookNotFoundError,
    BooksNotFoundError,
)


class ErrorMessageBookNotFound(BaseModel):
    detail: str = Field(example=BookNotFoundError.message)


class ErrorMessageBooksNotFound(BaseModel):
    detail: str = Field(example=BooksNotFoundError.message)


class ErrorMessageBookIsbnAlreadyExists(BaseModel):
    detail: str = Field(example=BookIsbnAlreadyExistsError.message)

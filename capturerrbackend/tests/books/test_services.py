from typing import Any

from sqlalchemy.orm import Session

from capturerrbackend.app.infrastructure.sqlite.book import BookQueryServiceImpl

# from ..app.infrastructure.dependencies import book_command_usecase, book_query_usecase
from capturerrbackend.app.usecase.book import (
    BookCommandUseCaseImpl,
    BookCreateModel,
    BookQueryService,
)


def test_book_query_service(
    db_fixture: Session,
    book_command_usecase: BookCommandUseCaseImpl,
    fake_book: dict[str, Any],
) -> None:
    book_query_service: BookQueryService = BookQueryServiceImpl(db_fixture)
    assert isinstance(book_query_service, BookQueryServiceImpl)

    book_model = BookCreateModel.model_validate(fake_book)
    book = book_command_usecase.create_book(
        book_model,
    )
    assert book is not None
    test_id = book.id
    fake_book["isbn"] = "978-1-445-85436-18"

    book_model2 = BookCreateModel.model_validate(fake_book)
    book = book_command_usecase.create_book(
        book_model2,
    )
    assert book is not None
    new_book = book_query_service.find_by_id(test_id)
    assert new_book is not None
    assert new_book.id == test_id

    books = book_query_service.find_all()
    assert len(books) == 2
    assert books[0].title == fake_book["title"]
    assert books[0].id == test_id

from capturerrbackend.app.domain.book.book_exception import (
    BookIsbnAlreadyExistsError,
    BookNotFoundError,
    BooksNotFoundError,
)
from capturerrbackend.app.usecase.book import (
    BookCommandUseCaseImpl,
    BookCreateModel,
    BookQueryUseCaseImpl,
    BookUpdateModel,
)

data = {
    "title": "Test Book",
    "read_page": 80,
    "isbn": "978-1-445-01022-1",
    "page": 123,
    "user_id": "vytxeTZskVKR7C7WgdSP3d",
}


def test_create_book(
    book_command_usecase: BookCommandUseCaseImpl,
    book_query_usecase: BookQueryUseCaseImpl,
) -> None:
    # Arrange

    book_model = BookCreateModel.model_validate(data)
    book = book_command_usecase.create_book(
        book_model,
    )
    assert book is not None

    all_books = book_query_usecase.fetch_books()
    assert len(all_books) > 0
    assert all_books[0].title == data["title"]


def test_create_book_duplicate_isbn(
    book_command_usecase: BookCommandUseCaseImpl,
    book_query_usecase: BookQueryUseCaseImpl,
) -> None:
    # Arrange

    book_model = BookCreateModel.model_validate(data)
    book = book_command_usecase.create_book(
        book_model,
    )
    assert book is not None
    try:
        # add the same book again
        book_command_usecase.create_book(
            book_model,
        )
        assert True is False
    except BookIsbnAlreadyExistsError as e:
        assert e.detail == BookIsbnAlreadyExistsError.detail
    except:
        assert True is False
        raise


def test_get_book(
    book_command_usecase: BookCommandUseCaseImpl,
    book_query_usecase: BookQueryUseCaseImpl,
) -> None:
    # Arrange

    book_model = BookCreateModel.model_validate(data)
    book = book_command_usecase.create_book(
        book_model,
    )
    assert book is not None
    abook = book_query_usecase.fetch_book_by_id(book.id)

    assert abook is not None
    assert abook.title == data["title"]
    assert abook.isbn == data["isbn"]


def test_get_book_no_books(
    book_command_usecase: BookCommandUseCaseImpl,
    book_query_usecase: BookQueryUseCaseImpl,
) -> None:
    # Arrange
    try:
        book_query_usecase.fetch_books()
        assert False
    except BooksNotFoundError as e:
        assert e.status_code == BooksNotFoundError.status_code
        assert e.detail == BooksNotFoundError.detail


def test_update_book_bad_id(
    book_command_usecase: BookCommandUseCaseImpl,
    book_query_usecase: BookQueryUseCaseImpl,
) -> None:
    # Arrange

    book_model = BookCreateModel.model_validate(data)
    book = book_command_usecase.create_book(
        book_model,
    )
    assert book is not None
    updated_book = BookUpdateModel.model_validate(book.model_dump())

    try:
        book_command_usecase.update_book("bad_id", updated_book)
        assert False
    except BookNotFoundError as e:
        assert e.status_code == BookNotFoundError.status_code
        assert e.detail == BookNotFoundError.detail

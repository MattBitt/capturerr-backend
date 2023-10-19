from capturerrbackend.app.domain.book.book_exception import BookIsbnAlreadyExistsError
from capturerrbackend.app.usecase.book import (
    BookCommandUseCaseImpl,
    BookCreateModel,
    BookQueryUseCaseImpl,
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
        assert e.message == BookIsbnAlreadyExistsError.message
    except:
        assert True is False
        raise

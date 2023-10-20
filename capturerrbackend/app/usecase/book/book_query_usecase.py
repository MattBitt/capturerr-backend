from abc import ABC, abstractmethod
from typing import List, Optional

from ...domain.book.book_exception import BookNotFoundError, BooksNotFoundError
from .book_query_model import BookReadModel
from .book_query_service import BookQueryService


class BookQueryUseCase(ABC):
    """BookQueryUseCase defines a query usecase inteface related Book entity."""

    @abstractmethod
    def fetch_book_by_id(self, book_id: str) -> Optional[BookReadModel]:
        """fetch_book_by_id fetches a book by id."""
        raise NotImplementedError

    @abstractmethod
    def fetch_books(self) -> List[BookReadModel]:
        """fetch_books fetches books."""
        raise NotImplementedError

    @abstractmethod
    def fetch_books_by_user_id(self, user_id: str) -> List[BookReadModel]:
        """fetch_books_by_user_id fetches books by user id."""
        raise NotImplementedError


class BookQueryUseCaseImpl(BookQueryUseCase):
    """BookQueryUseCaseImpl implements a query usecases related Book entity."""

    def __init__(self, book_query_service: BookQueryService):
        self.book_query_service: BookQueryService = book_query_service

    def fetch_book_by_id(self, book_id: str) -> Optional[BookReadModel]:
        """fetch_book_by_id fetches a book by id."""
        try:
            book = self.book_query_service.find_by_id(book_id)
            if book is None:
                raise BookNotFoundError
        except:
            raise

        return book

    def fetch_books(self) -> List[BookReadModel]:
        """fetch_books fetches books."""
        try:
            books = self.book_query_service.find_all()
            if not books:
                raise BooksNotFoundError
        except:
            raise

        return books

    def fetch_books_by_user_id(self, user_id: str) -> List[BookReadModel]:
        """fetch_books_by_user_id fetches books by user id."""
        try:
            books = self.book_query_service.find_by_user_id(user_id)
            if books is None:
                raise BooksNotFoundError
        except:
            raise

        return books

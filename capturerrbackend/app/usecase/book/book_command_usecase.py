from abc import ABC, abstractmethod
from typing import Optional, cast
from uuid import uuid4

from ...domain.book.book import Book
from ...domain.book.book_exception import BookIsbnAlreadyExistsError, BookNotFoundError
from ...domain.book.book_repository import BookRepository
from ...domain.book.isbn import Isbn
from .book_command_model import BookCreateModel, BookUpdateModel
from .book_query_model import BookReadModel


class BookCommandUseCaseUnitOfWork(ABC):
    """BookCommandUseCaseUnitOfWork defines an interface based
    on Unit of Work pattern."""

    book_repository: BookRepository

    @abstractmethod
    def begin(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class BookCommandUseCase(ABC):
    """BookCommandUseCase defines a command usecase inteface related Book entity."""

    @abstractmethod
    def create_book(self, data: BookCreateModel) -> BookReadModel:
        raise NotImplementedError

    @abstractmethod
    def update_book(
        self,
        book_id: str,
        data: BookUpdateModel,
    ) -> Optional[BookReadModel]:
        raise NotImplementedError

    @abstractmethod
    def delete_book_by_id(self, book_id: str) -> None:
        raise NotImplementedError


class BookCommandUseCaseImpl(BookCommandUseCase):
    """BookCommandUseCaseImpl implements a command usecases related Book entity."""

    def __init__(
        self,
        uow: BookCommandUseCaseUnitOfWork,
    ):
        self.uow: BookCommandUseCaseUnitOfWork = uow

    def create_book(self, data: BookCreateModel) -> BookReadModel:
        try:
            uuid = uuid4().hex
            isbn = Isbn(data.isbn)
            book = Book(
                book_id=uuid,
                isbn=isbn,
                title=data.title,
                page=data.page,
                user_id=data.user_id,
            )

            existing_book = self.uow.book_repository.find_by_isbn(isbn.value)
            if existing_book is not None:
                raise BookIsbnAlreadyExistsError

            self.uow.book_repository.create(book)
            self.uow.commit()

            created_book = self.uow.book_repository.find_by_id(uuid)
            return BookReadModel.from_entity(cast(Book, created_book))
        except:
            self.uow.rollback()
            raise

    def update_book(
        self,
        book_id: str,
        data: BookUpdateModel,
    ) -> Optional[BookReadModel]:
        try:
            existing_book = self.uow.book_repository.find_by_id(book_id)
            if existing_book is None:
                raise BookNotFoundError

            book = Book(
                book_id=book_id,
                isbn=Isbn(data.isbn),
                title=data.title,
                page=data.page,
                user_id=data.user_id,
                read_page=data.read_page,
            )

            self.uow.book_repository.update(book)

            updated_book = self.uow.book_repository.find_by_id(book.book_id)

            self.uow.commit()
        except:
            self.uow.rollback()
            raise

        return BookReadModel.from_entity(cast(Book, updated_book))

    def delete_book_by_id(self, book_id: str) -> None:
        try:
            existing_book = self.uow.book_repository.find_by_id(book_id)
            if existing_book is None:
                raise BookNotFoundError

            self.uow.book_repository.delete_by_id(book_id)

            self.uow.commit()
        except:
            self.uow.rollback()
            raise

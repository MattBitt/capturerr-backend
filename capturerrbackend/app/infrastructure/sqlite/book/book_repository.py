from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from capturerrbackend.app.domain.book.book import Book
from capturerrbackend.app.domain.book.book_repository import BookRepository
from capturerrbackend.app.usecase.book import BookCommandUseCaseUnitOfWork

from .book_dto import BookDTO


class BookRepositoryImpl(BookRepository):
    """BookRepositoryImpl implements CRUD operations related Book
    entity using SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def find_by_id(self, book_id: str) -> Optional[Book]:
        try:
            book_dto = self.session.query(BookDTO).filter_by(id=book_id).one()
        except NoResultFound:
            return None
        except:
            raise

        return book_dto.to_entity()

    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        try:
            book_dto = self.session.query(BookDTO).filter_by(isbn=isbn).one()
        except NoResultFound:
            return None
        except:
            raise

        return book_dto.to_entity()

    def create(self, book: Book) -> None:
        book_dto = BookDTO.from_entity(book)
        try:
            self.session.add(book_dto)
        except:
            raise

    def update(self, book: Book) -> None:
        book_dto = BookDTO.from_entity(book)
        try:
            _book = self.session.query(BookDTO).filter_by(id=book_dto.id).one()
            _book.title = book_dto.title
            _book.page = book_dto.page
            _book.read_page = book_dto.read_page
            _book.updated_at = book_dto.updated_at
            _book.isbn = book_dto.isbn
        except:
            raise

    def delete_by_id(self, book_id: str) -> None:
        try:
            self.session.query(BookDTO).filter_by(id=book_id).delete()
        except:
            raise


class BookCommandUseCaseUnitOfWorkImpl(BookCommandUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        book_repository: BookRepository,
    ):
        self.session: Session = session
        self.book_repository: BookRepository = book_repository

    def begin(self) -> None:
        self.session.begin()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

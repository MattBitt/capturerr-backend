from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from capturerrbackend.app.domain.book.book import Book
from capturerrbackend.app.domain.book.isbn import Isbn
from capturerrbackend.app.infrastructure.sqlite.database import Base
from capturerrbackend.app.usecase.book import BookReadModel

if TYPE_CHECKING:
    from capturerrbackend.app.infrastructure.sqlite import UserDTO


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class BookDTO(Base):
    """BookDTO is a data transfer object associated with Book entity."""

    __tablename__ = "book"
    isbn: Mapped[str] = mapped_column(String(17), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    page: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserDTO"] = relationship(back_populates="books")

    read_page: Mapped[int] = mapped_column(nullable=False, default=0)

    def to_entity(self) -> Book:
        return Book(
            book_id=self.id,
            isbn=Isbn(self.isbn),
            title=self.title,
            page=self.page,
            user_id=self.user_id,
            read_page=self.read_page,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_read_model(self) -> BookReadModel:
        return BookReadModel(
            id=self.id,
            isbn=self.isbn,
            title=self.title,
            page=self.page,
            user_id=self.user_id,
            read_page=self.read_page,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(book: Book) -> "BookDTO":
        now = unixtimestamp()
        return BookDTO(
            id=book.book_id,
            isbn=book.isbn.value,
            title=book.title,
            page=book.page,
            user_id=book.user_id,
            read_page=book.read_page,
            created_at=now,
            updated_at=now,
        )

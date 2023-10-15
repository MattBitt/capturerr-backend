from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.orm import Session

from ..app.domain.book.book_exception import (
    BookIsbnAlreadyExistsError,
    BookNotFoundError,
    BooksNotFoundError,
)
from ..app.domain.book.book_repository import BookRepository
from ..app.infrastructure.dependencies import get_sync_session
from ..app.infrastructure.sqlite.book import (
    BookCommandUseCaseUnitOfWorkImpl,
    BookQueryServiceImpl,
    BookRepositoryImpl,
)

# from ..app.infrastructure.dependencies import book_command_usecase, book_query_usecase
from ..app.presentation.schema.book.book_error_message import (
    ErrorMessageBookIsbnAlreadyExists,
    ErrorMessageBookNotFound,
    ErrorMessageBooksNotFound,
)
from ..app.usecase.book import (
    BookCommandUseCase,
    BookCommandUseCaseImpl,
    BookCommandUseCaseUnitOfWork,
    BookCreateModel,
    BookQueryService,
    BookQueryUseCase,
    BookQueryUseCaseImpl,
    BookReadModel,
    BookUpdateModel,
)

router = APIRouter()


def book_query_usecase(
    session: Session = Depends(get_sync_session),
) -> BookQueryUseCase:
    """Get a book query use case."""
    book_query_service: BookQueryService = BookQueryServiceImpl(session)
    return BookQueryUseCaseImpl(book_query_service)


def book_command_usecase(
    session: Session = Depends(get_sync_session),
) -> BookCommandUseCase:
    """Get a book command use case."""
    book_repository: BookRepository = BookRepositoryImpl(session)
    uow: BookCommandUseCaseUnitOfWork = BookCommandUseCaseUnitOfWorkImpl(
        session,
        book_repository=book_repository,
    )
    return BookCommandUseCaseImpl(uow)


@router.post(
    "/books",
    response_model=BookReadModel,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorMessageBookIsbnAlreadyExists,
        },
    },
)
def create_book(
    data: BookCreateModel,
    book_command_usecase: BookCommandUseCase = Depends(book_command_usecase),
) -> Optional[BookReadModel]:
    """Create a book."""
    try:
        book = book_command_usecase.create_book(data)
    except BookIsbnAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return book


@router.get(
    "/books",
    response_model=List[BookReadModel],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBooksNotFound,
        },
    },
)
async def get_books(
    book_query_usecase: BookQueryUseCase = Depends(book_query_usecase),
) -> List[BookReadModel]:
    """Get a list of books."""
    try:
        books = book_query_usecase.fetch_books()

    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if len(books) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BooksNotFoundError.message,
        )

    return books


@router.get(
    "/books/{book_id}",
    response_model=BookReadModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBookNotFound,
        },
    },
)
async def get_book(
    book_id: str,
    book_query_usecase: BookQueryUseCase = Depends(book_query_usecase),
) -> Optional[BookReadModel]:
    """Get a book."""
    try:
        book = book_query_usecase.fetch_book_by_id(book_id)
    except BookNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.message,
        )
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return book


@router.put(
    "/books/{book_id}",
    response_model=BookReadModel,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBookNotFound,
        },
    },
)
async def update_book(
    book_id: str,
    data: BookUpdateModel,
    book_command_usecase: BookCommandUseCase = Depends(book_command_usecase),
) -> Optional[BookReadModel]:
    """Update a book."""
    try:
        updated_book = book_command_usecase.update_book(book_id, data)
    except BookNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.message,
        )
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return updated_book


@router.delete(
    "/books/{book_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBookNotFound,
        },
    },
)
async def delete_book(
    book_id: str,
    book_command_usecase: BookCommandUseCase = Depends(book_command_usecase),
) -> None:
    """Delete a bool."""
    try:
        book_command_usecase.delete_book_by_id(book_id)
    except BookNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.message,
        )
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

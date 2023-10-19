from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from capturerrbackend.app.domain.book.book_exception import (
    BookIsbnAlreadyExistsError,
    BookNotFoundError,
    BooksNotFoundError,
)
from capturerrbackend.app.domain.user.user_exception import UserNotFoundError
from capturerrbackend.app.infrastructure.dependencies import (
    book_command_usecase,
    book_query_usecase,
    get_current_active_user,
    user_query_usecase,
)
from capturerrbackend.app.presentation.schema.book.book_error_message import (
    ErrorMessageBookIsbnAlreadyExists,
    ErrorMessageBookNotFound,
    ErrorMessageBooksNotFound,
)
from capturerrbackend.app.usecase.book import (
    BookCommandUseCase,
    BookCreateModel,
    BookQueryUseCase,
    BookReadModel,
    BookUpdateModel,
)
from capturerrbackend.app.usecase.user import UserQueryUseCase, UserReadModel

router = APIRouter()


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
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    user_query_usecase: Annotated[UserQueryUseCase, Depends(user_query_usecase)],
    book_command_usecase: Annotated[BookCommandUseCase, Depends(book_command_usecase)],
) -> Optional[BookReadModel]:
    """Create a book."""
    try:
        if current_user is None:
            raise UserNotFoundError
        user = user_query_usecase.fetch_user_by_id(current_user.id)
        if user is None:
            raise UserNotFoundError
        data.user_id = user.id
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

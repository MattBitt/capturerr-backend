from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from capturerrbackend.api.custom_error_route_handler import CustomErrorRouteHandler
from capturerrbackend.app.domain.user.user_exception import UserNotFoundError
from capturerrbackend.app.infrastructure.dependencies import (
    book_command_usecase,
    book_query_usecase,
    get_current_active_user,
    user_query_usecase,
)
from capturerrbackend.app.usecase.book import (
    BookCommandUseCase,
    BookCreateModel,
    BookQueryUseCase,
    BookReadModel,
    BookUpdateModel,
)
from capturerrbackend.app.usecase.user import UserQueryUseCase, UserReadModel

router = APIRouter(route_class=CustomErrorRouteHandler)


@router.post(
    "/books",
    response_model=BookReadModel,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    data: BookCreateModel,
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    user_query_usecase: Annotated[UserQueryUseCase, Depends(user_query_usecase)],
    book_command_usecase: Annotated[BookCommandUseCase, Depends(book_command_usecase)],
) -> Optional[BookReadModel]:
    """Create a book."""
    # try:
    user = user_query_usecase.fetch_user_by_id(current_user.id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=UserNotFoundError.detail,
        )
    data.user_id = user.id
    book = book_command_usecase.create_book(data)
    return book
    # except BookIsbnAlreadyExistsError as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail=e.message,
    #     )
    # except Exception as e:
    #     logger.error(e)
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #     )

    # return book


@router.get(
    "/books",
    response_model=List[BookReadModel],
    status_code=status.HTTP_200_OK,
)
#
async def get_books(
    book_query_usecase: BookQueryUseCase = Depends(book_query_usecase),
) -> List[BookReadModel]:
    """Get a list of books."""
    return book_query_usecase.fetch_books()


@router.get(
    "/books/{book_id}",
    response_model=BookReadModel,
    status_code=status.HTTP_200_OK,
)
async def get_book(
    book_id: str,
    book_query_usecase: BookQueryUseCase = Depends(book_query_usecase),
) -> Optional[BookReadModel]:
    """Get a book."""
    return book_query_usecase.fetch_book_by_id(book_id)


@router.put(
    "/books/{book_id}",
    response_model=BookReadModel,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_book(
    book_id: str,
    data: BookUpdateModel,
    book_command_usecase: BookCommandUseCase = Depends(book_command_usecase),
) -> Optional[BookReadModel]:
    """Update a book."""
    return book_command_usecase.update_book(book_id, data)


@router.delete(
    "/books/{book_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_book(
    book_id: str,
    book_command_usecase: BookCommandUseCase = Depends(book_command_usecase),
) -> None:
    """Delete a book."""
    book_command_usecase.delete_book_by_id(book_id)

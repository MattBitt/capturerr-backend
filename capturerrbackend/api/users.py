from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from capturerrbackend.app.domain.book.book_exception import BooksNotFoundError
from capturerrbackend.app.domain.custom_exception import CustomException
from capturerrbackend.app.domain.user.user_exception import (
    UserNotFoundError,
    UserNotSuperError,
)
from capturerrbackend.app.infrastructure.dependencies import (
    book_query_usecase,
    get_current_active_super_user,
    get_current_active_user,
    user_command_usecase,
    user_query_usecase,
)
from capturerrbackend.app.usecase.book import BookQueryUseCase, BookReadModel
from capturerrbackend.app.usecase.user import (
    Token,
    UserCommandUseCase,
    UserCreateModel,
    UserLoginModel,
    UserQueryUseCase,
    UserReadModel,
    UserUpdateModel,
    create_access_token,
)

router = APIRouter()


@router.post(
    "/users",
    response_model=None,  # UserReadModel,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    data: UserCreateModel,
    user_command_usecase: Annotated[UserCommandUseCase, Depends(user_command_usecase)],
) -> Optional[UserReadModel]:
    """Create a user."""
    try:
        user = user_command_usecase.create_user(data)
    except CustomException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.detail,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return user


@router.get(
    "/users",
    response_model=List[UserReadModel],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    active_user: UserReadModel = Depends(get_current_active_user),
    user_query_usecase: UserQueryUseCase = Depends(user_query_usecase),
) -> List[UserReadModel]:
    """Get a list of users."""
    logger.debug(f"Getting all users.  Requested by {active_user.user_name}")
    try:
        users = user_query_usecase.fetch_users()
    except CustomException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.detail,
        )
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return users


@router.get(
    "/users/me",
    response_model=UserReadModel,
    status_code=status.HTTP_200_OK,
)
async def get_me(
    active_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    user_query_usecase: Annotated[UserQueryUseCase, Depends(user_query_usecase)],
) -> Optional[UserReadModel]:
    """Get a user."""
    logger.debug("In get_me route")
    try:
        user = user_query_usecase.fetch_user_by_user_name(active_user.user_name)
    except CustomException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.detail,
        )
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return user


@router.get(
    "/users/{user_id}",
    response_model=UserReadModel,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: str,
    admin_user: Annotated[UserReadModel, Depends(get_current_active_super_user)],
    user_query_usecase: Annotated[UserQueryUseCase, Depends(user_query_usecase)],
) -> Optional[UserReadModel]:
    """Get a user."""
    logger.debug("This will only be logged if the user is an admin.")
    try:
        user = user_query_usecase.fetch_user_by_id(user_id)
    except CustomException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.detail,
        )
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return user


@router.put(
    "/users/{user_id}",
    response_model=UserReadModel,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_user(
    user_id: str,
    data: UserUpdateModel,
    user_command_usecase: Annotated[UserCommandUseCase, Depends(user_command_usecase)],
) -> Optional[UserReadModel]:
    """Update a user."""
    try:
        updated_user = user_command_usecase.update_user(user_id, data)
    except CustomException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.detail,
        )
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return updated_user


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_user(
    user_id: str,
    user_command_usecase: Annotated[UserCommandUseCase, Depends(user_command_usecase)],
) -> None:
    """Delete a bool."""
    try:
        user_command_usecase.delete_user_by_id(user_id)
    except CustomException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.detail,
        )
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post(
    "/users/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    user: UserLoginModel,
    user_query_usecase: Annotated[UserQueryUseCase, Depends(user_query_usecase)],
    user_command_usecase: Annotated[UserCommandUseCase, Depends(user_command_usecase)],
) -> Token:
    """Get a user."""
    try:
        potential_user = user_query_usecase.login_user(user)
        if potential_user is None:
            raise UserNotFoundError
        token = Token(
            access_token=create_access_token(potential_user.model_dump()),
            token_type="bearer",
        )
    except CustomException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.detail,
        )
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return token


@router.get(
    "/users/{user_id}/books",
    response_model=list[BookReadModel],
    status_code=status.HTTP_200_OK,
)
async def get_user_books(
    user_id: str,
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    book_query_usecase: Annotated[BookQueryUseCase, Depends(book_query_usecase)],
    user_query_usecase: Annotated[UserQueryUseCase, Depends(user_query_usecase)],
) -> Optional[list[BookReadModel]]:
    if (current_user.id != user_id) and (current_user.is_superuser is False):
        raise UserNotSuperError
    try:
        user = user_query_usecase.fetch_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError
    except CustomException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.detail,
        )
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    try:
        books = book_query_usecase.fetch_books_by_user_id(user.id)
    except BooksNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.detail,
        )
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return books

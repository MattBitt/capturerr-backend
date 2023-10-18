from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.orm import Session

from capturerrbackend.app.domain.user.user_exception import (
    UserAlreadyExistsError,
    UserBadCredentialsError,
    UserNotFoundError,
    UsersNotFoundError,
)
from capturerrbackend.app.domain.user.user_repository import UserRepository
from capturerrbackend.app.infrastructure.dependencies import (
    get_current_active_user,
    get_sync_session,
)
from capturerrbackend.app.infrastructure.sqlite.user import (
    UserCommandUseCaseUnitOfWorkImpl,
    UserQueryServiceImpl,
    UserRepositoryImpl,
)

# from ..app.infrastructure.dependencies import user_command_usecase, user_query_usecase
from capturerrbackend.app.presentation.schema.user.user_error_message import (
    ErrorMessageBadCredentials,
    ErrorMessageUserAlreadyExists,
    ErrorMessageUserNotFound,
    ErrorMessageUsersNotFound,
)
from capturerrbackend.app.usecase.user import (
    Token,
    UserCommandUseCase,
    UserCommandUseCaseImpl,
    UserCommandUseCaseUnitOfWork,
    UserCreateModel,
    UserLoginModel,
    UserQueryService,
    UserQueryUseCase,
    UserQueryUseCaseImpl,
    UserReadModel,
    UserUpdateModel,
    create_access_token,
)

router = APIRouter()


def user_query_usecase(
    session: Session = Depends(get_sync_session),
) -> UserQueryUseCase:
    """Get a user query use case."""
    user_query_service: UserQueryService = UserQueryServiceImpl(session)
    return UserQueryUseCaseImpl(user_query_service)


def user_command_usecase(
    session: Session = Depends(get_sync_session),
) -> UserCommandUseCase:
    """Get a user command use case."""
    user_repository: UserRepository = UserRepositoryImpl(session)
    uow: UserCommandUseCaseUnitOfWork = UserCommandUseCaseUnitOfWorkImpl(
        session,
        user_repository=user_repository,
    )
    return UserCommandUseCaseImpl(uow)


@router.post(
    "/users",
    response_model=UserReadModel,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorMessageUserAlreadyExists,
        },
    },
)
def create_user(
    data: UserCreateModel,
    user_command_usecase: UserCommandUseCase = Depends(user_command_usecase),
) -> Optional[UserReadModel]:
    """Create a user."""
    try:
        user = user_command_usecase.create_user(data)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
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
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageUsersNotFound,
        },
    },
)
async def get_users(
    active_user: UserReadModel = Depends(get_current_active_user),
    user_query_usecase: UserQueryUseCase = Depends(user_query_usecase),
) -> List[UserReadModel]:
    """Get a list of users."""
    logger.debug(f"Getting all users.  Requested by {active_user.user_name}")
    try:
        users = user_query_usecase.fetch_users()

    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if len(users) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=UsersNotFoundError.message,
        )

    return users


@router.get(
    "/users/me",
    response_model=UserReadModel,
    status_code=status.HTTP_200_OK,
)
async def get_me(
    active_user: UserReadModel = Depends(get_current_active_user),
    user_query_usecase: UserQueryUseCase = Depends(user_query_usecase),
) -> Optional[UserReadModel]:
    """Get a user."""
    logger.debug("In get_me route")
    try:
        user = user_query_usecase.fetch_user_by_user_name(active_user.user_name)
    except UserNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.message,
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
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageUserNotFound,
        },
    },
)
async def get_user(
    user_id: str,
    user_query_usecase: UserQueryUseCase = Depends(user_query_usecase),
) -> Optional[UserReadModel]:
    """Get a user."""
    try:
        user = user_query_usecase.fetch_user_by_id(user_id)
    except UserNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.message,
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
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageUserNotFound,
        },
    },
)
async def update_user(
    user_id: str,
    data: UserUpdateModel,
    user_command_usecase: UserCommandUseCase = Depends(user_command_usecase),
) -> Optional[UserReadModel]:
    """Update a user."""
    try:
        updated_user = user_command_usecase.update_user(user_id, data)
    except UserNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.message,
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
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageUserNotFound,
        },
    },
)
async def delete_user(
    user_id: str,
    user_command_usecase: UserCommandUseCase = Depends(user_command_usecase),
) -> None:
    """Delete a bool."""
    try:
        user_command_usecase.delete_user_by_id(user_id)
    except UserNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.message,
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
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorMessageBadCredentials,
        },
    },
)
async def login_user(
    user: UserLoginModel,
    user_query_usecase: UserQueryUseCase = Depends(user_query_usecase),
    user_command_usecase: UserCommandUseCase = Depends(user_command_usecase),
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
    except UserBadCredentialsError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err.message,
        )
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return token

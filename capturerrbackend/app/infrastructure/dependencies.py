from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from loguru import logger
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import Session, sessionmaker

from capturerrbackend.app.infrastructure.sqlite.user import UserQueryServiceImpl
from capturerrbackend.app.presentation.schema.user.user_error_message import (
    UserBadCredentialsError,
    UserNotFoundError,
)
from capturerrbackend.app.usecase.user.user_auth_service import TokenData
from capturerrbackend.app.usecase.user.user_query_model import UserReadModel
from capturerrbackend.app.usecase.user.user_query_service import UserQueryService
from capturerrbackend.app.usecase.user.user_query_usecase import (
    UserQueryUseCase,
    UserQueryUseCaseImpl,
)
from capturerrbackend.config.configurator import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def get_sync_session():  # type: ignore
    engine = create_engine(str(config.db_url), echo=config.db_echo)
    factory = sessionmaker(engine)
    with factory() as session:
        try:
            yield session
            session.commit()
        except exc.SQLAlchemyError as error:
            session.rollback()
            logger.error(error)
            raise


def user_query_usecase(
    db_fixture: Session = Depends(get_sync_session),
) -> UserQueryUseCase:
    """Get a user query use case."""
    user_query_service: UserQueryService = UserQueryServiceImpl(db_fixture)
    return UserQueryUseCaseImpl(user_query_service)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_query: Annotated[UserQueryUseCase, Depends(user_query_usecase)],
) -> UserReadModel:
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        user_name: str = payload.get("user_name")
        if user_name is None:
            raise UserBadCredentialsError
        td = TokenData(user_name=user_name)
    except JWTError:
        raise UserBadCredentialsError
    if td.user_name is None:
        raise UserBadCredentialsError
    user = user_query.fetch_user_by_user_name(td.user_name)
    if user is None:
        raise UserBadCredentialsError
    return user


def get_current_active_user(
    current_user: Annotated[UserReadModel, Depends(get_current_user)],
) -> UserReadModel:
    if not current_user.is_active:
        raise UserNotFoundError
    return current_user


# def book_query_usecase(
#     session: Session = get_sync_session(),
# ) -> BookQueryUseCase:
#     """Get a book query use case."""
#     book_query_service: BookQueryService = BookQueryServiceImpl(session)
#     return BookQueryUseCaseImpl(book_query_service)


# def book_command_usecase(
#     session: Session,
# ) -> BookCommandUseCase:
#     """Get a book command use case."""
#     book_repository: BookRepository = BookRepositoryImpl(session)
#     uow: BookCommandUseCaseUnitOfWork = BookCommandUseCaseUnitOfWorkImpl(
#         session,
#         book_repository=book_repository,
#     )
#     return BookCommandUseCaseImpl(uow)

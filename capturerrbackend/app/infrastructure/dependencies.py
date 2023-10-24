from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from loguru import logger
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import Session, sessionmaker

from capturerrbackend.app.domain.book.book_repository import BookRepository
from capturerrbackend.app.domain.capture.capture_repository import CaptureRepository
from capturerrbackend.app.domain.tag.tag_repository import TagRepository
from capturerrbackend.app.domain.user.user_exception import (
    UserBadCredentialsError,
    UserNotFoundError,
    UserNotSuperError,
)
from capturerrbackend.app.domain.user.user_repository import UserRepository
from capturerrbackend.app.infrastructure.sqlite.book import (
    BookCommandUseCaseUnitOfWorkImpl,
    BookQueryServiceImpl,
    BookRepositoryImpl,
)
from capturerrbackend.app.infrastructure.sqlite.capture import (
    CaptureCommandUseCaseUnitOfWorkImpl,
    CaptureQueryServiceImpl,
    CaptureRepositoryImpl,
)
from capturerrbackend.app.infrastructure.sqlite.tag import (
    TagCommandUseCaseUnitOfWorkImpl,
    TagQueryServiceImpl,
    TagRepositoryImpl,
)
from capturerrbackend.app.infrastructure.sqlite.user import (
    UserCommandUseCaseUnitOfWorkImpl,
    UserQueryServiceImpl,
    UserRepositoryImpl,
)
from capturerrbackend.app.usecase.book import (
    BookCommandUseCase,
    BookCommandUseCaseImpl,
    BookCommandUseCaseUnitOfWork,
    BookQueryService,
    BookQueryUseCase,
    BookQueryUseCaseImpl,
)
from capturerrbackend.app.usecase.capture import (
    CaptureCommandUseCase,
    CaptureCommandUseCaseImpl,
    CaptureCommandUseCaseUnitOfWork,
    CaptureQueryService,
    CaptureQueryUseCase,
    CaptureQueryUseCaseImpl,
)
from capturerrbackend.app.usecase.tag import (
    TagCommandUseCase,
    TagCommandUseCaseImpl,
    TagCommandUseCaseUnitOfWork,
    TagQueryService,
    TagQueryUseCase,
    TagQueryUseCaseImpl,
)
from capturerrbackend.app.usecase.user import (
    TokenData,
    UserCommandUseCase,
    UserCommandUseCaseImpl,
    UserCommandUseCaseUnitOfWork,
    UserQueryService,
    UserQueryUseCase,
    UserQueryUseCaseImpl,
    UserReadModel,
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


def user_command_usecase(
    db_fixture: Annotated[Session, Depends(get_sync_session)],
) -> UserCommandUseCase:
    """Get a user command use case."""
    user_repository: UserRepository = UserRepositoryImpl(db_fixture)
    uow: UserCommandUseCaseUnitOfWork = UserCommandUseCaseUnitOfWorkImpl(
        db_fixture,
        user_repository=user_repository,
    )
    return UserCommandUseCaseImpl(uow)


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


def get_current_active_super_user(
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
) -> UserReadModel:
    if not current_user.is_superuser:
        raise UserNotSuperError
    return current_user


def book_query_usecase(
    session: Annotated[Session, Depends(get_sync_session)],
) -> BookQueryUseCase:
    """Get a book query use case."""
    book_query_service: BookQueryService = BookQueryServiceImpl(session)
    return BookQueryUseCaseImpl(book_query_service)


def book_command_usecase(
    session: Annotated[Session, Depends(get_sync_session)],
) -> BookCommandUseCase:
    """Get a book command use case."""
    book_repository: BookRepository = BookRepositoryImpl(session)
    uow: BookCommandUseCaseUnitOfWork = BookCommandUseCaseUnitOfWorkImpl(
        session,
        book_repository=book_repository,
    )
    return BookCommandUseCaseImpl(uow)


def tag_query_usecase(
    session: Annotated[Session, Depends(get_sync_session)],
) -> TagQueryUseCase:
    """Get a tag query use case."""
    tag_query_service: TagQueryService = TagQueryServiceImpl(session)
    return TagQueryUseCaseImpl(tag_query_service)


def tag_command_usecase(
    session: Annotated[Session, Depends(get_sync_session)],
) -> TagCommandUseCase:
    """Get a tag command use case."""
    tag_repository: TagRepository = TagRepositoryImpl(session)
    uow: TagCommandUseCaseUnitOfWork = TagCommandUseCaseUnitOfWorkImpl(
        session,
        tag_repository=tag_repository,
    )
    return TagCommandUseCaseImpl(uow)


def capture_query_usecase(
    session: Annotated[Session, Depends(get_sync_session)],
) -> CaptureQueryUseCase:
    """Get a capture query use case."""
    capture_query_service: CaptureQueryService = CaptureQueryServiceImpl(session)
    return CaptureQueryUseCaseImpl(capture_query_service)


def capture_command_usecase(
    session: Annotated[Session, Depends(get_sync_session)],
) -> CaptureCommandUseCase:
    """Get a capture command use case."""
    capture_repository: CaptureRepository = CaptureRepositoryImpl(session)
    uow: CaptureCommandUseCaseUnitOfWork = CaptureCommandUseCaseUnitOfWorkImpl(
        session,
        capture_repository=capture_repository,
    )
    return CaptureCommandUseCaseImpl(uow)

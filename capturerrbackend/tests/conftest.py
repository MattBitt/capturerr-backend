from collections.abc import AsyncIterator, Iterator
from datetime import datetime
from typing import Annotated, Any

import pytest
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from httpx import AsyncClient
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from capturerrbackend.app.application import get_app
from capturerrbackend.app.domain.book.book_repository import BookRepository
from capturerrbackend.app.domain.capture.capture_repository import CaptureRepository
from capturerrbackend.app.domain.tag.tag_repository import TagRepository
from capturerrbackend.app.domain.user.user_repository import UserRepository
from capturerrbackend.app.infrastructure.dependencies import (
    book_command_usecase as new_bcu,
)
from capturerrbackend.app.infrastructure.dependencies import (
    get_current_active_super_user,
    get_current_active_user,
    get_sync_session,
)
from capturerrbackend.app.infrastructure.dependencies import (
    tag_command_usecase as new_tcu,
)
from capturerrbackend.app.infrastructure.dependencies import (
    user_command_usecase as new_ucu,
)
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
from capturerrbackend.app.infrastructure.sqlite.database import Base
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
    BookCreateModel,
    BookQueryService,
    BookQueryUseCase,
    BookQueryUseCaseImpl,
    BookReadModel,
)
from capturerrbackend.app.usecase.capture import (
    CaptureCommandUseCase,
    CaptureCommandUseCaseImpl,
    CaptureCommandUseCaseUnitOfWork,
    CaptureCreateModel,
    CaptureQueryService,
    CaptureQueryUseCase,
    CaptureQueryUseCaseImpl,
    CaptureReadModel,
)
from capturerrbackend.app.usecase.tag import (
    TagCommandUseCase,
    TagCommandUseCaseImpl,
    TagCommandUseCaseUnitOfWork,
    TagCreateModel,
    TagQueryService,
    TagQueryUseCase,
    TagQueryUseCaseImpl,
    TagReadModel,
)
from capturerrbackend.app.usecase.user import (
    UserCommandUseCase,
    UserCommandUseCaseImpl,
    UserCommandUseCaseUnitOfWork,
    UserCreateModel,
    UserQueryService,
    UserQueryUseCase,
    UserQueryUseCaseImpl,
    UserReadModel,
)
from capturerrbackend.config.configurator import config
from capturerrbackend.utils.utils import get_int_timestamp

engine = create_engine(str(config.db_url), connect_args={"check_same_thread": False})
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def fake_book() -> dict[str, Any]:
    return {
        "title": "Test Book",
        "read_page": 80,
        "isbn": "978-1-445-85436-1",
        "page": 123,
        "created_at": get_int_timestamp(datetime.now()),
        "updated_at": get_int_timestamp(datetime.now()),
        "deleted_at": None,
        "user_id": "vytxeTZskVKR7C7WgdSP3d",
    }


@pytest.fixture
def fake_user() -> dict[str, Any]:
    return {
        "user_name": "matt",
        "first_name": "Matt",
        "last_name": "Bittinger",
        "email": "matt@bittfurst.xyz",
        "password": "matt",
        "is_superuser": False,
        "created_at": get_int_timestamp(datetime.now()),
        "updated_at": get_int_timestamp(datetime.now()),
        "deleted_at": None,
    }


@pytest.fixture
def fake_super_user() -> dict[str, Any]:
    return {
        "user_name": "admin",
        "first_name": "Admin",
        "last_name": "Strator",
        "email": "admin@bittfurst.xyz",
        "password": "admin",
        "is_superuser": True,
        "created_at": get_int_timestamp(datetime.now()),
        "updated_at": get_int_timestamp(datetime.now()),
        "deleted_at": None,
    }


@pytest.fixture
def fake_tag() -> dict[str, Any]:
    return {
        "text": "test-monotone",
        "created_at": get_int_timestamp(datetime.now()),
        "updated_at": get_int_timestamp(datetime.now()),
        "deleted_at": None,
        "user_id": "vytxeTZskVKR7C7WgdSP3d",
    }


@pytest.fixture
def fake_capture() -> dict[str, Any]:
    return {
        "entry": "Still coding at 530 in the am.",
        "entry_type": "asdf",
        "notes": "I'm way too old for this shit!",
        "location": "Home",
        "flagged": "false",
        "priority": "high",
        "happened_at": get_int_timestamp(datetime.now()),
        "due_date": get_int_timestamp(datetime.now()),
        "created_at": get_int_timestamp(datetime.now()),
        "updated_at": get_int_timestamp(datetime.now()),
        "deleted_at": None,
        "user_id": "vytxeTZskVKR7C7WgdSP3d",
        "capture_id": "y8ghf;fldsjrewqpiog",
    }


@pytest.fixture
def new_user_in_db(
    fake_user: dict[str, Any],
    user_command_usecase: Annotated[UserCommandUseCase, Depends(new_ucu)],
) -> UserReadModel:
    ...
    user = UserCreateModel.model_validate(fake_user)

    user_in_db = user_command_usecase.create_user(user)

    assert user_in_db is not None
    return user_in_db


@pytest.fixture
def new_super_user_in_db(
    fake_super_user: dict[str, Any],
    user_command_usecase: Annotated[UserCommandUseCase, Depends(new_ucu)],
) -> UserReadModel:
    ...
    user = UserCreateModel.model_validate(fake_super_user)

    user_in_db = user_command_usecase.create_user(user)

    assert user_in_db is not None
    assert user_in_db.is_superuser is True
    return user_in_db


@pytest.fixture
def new_book_in_db(
    new_user_in_db: UserReadModel,
    fake_book: dict[str, Any],
    book_command_usecase: Annotated[BookCommandUseCase, Depends(new_bcu)],
) -> BookReadModel:
    ...
    fake_book["user_id"] = new_user_in_db.id
    book = BookCreateModel.model_validate(fake_book)

    book_in_db = book_command_usecase.create_book(book)
    assert book_in_db is not None
    return book_in_db


@pytest.fixture
def new_tag_in_db(
    new_user_in_db: UserReadModel,
    fake_tag: dict[str, Any],
    tag_command_usecase: Annotated[TagCommandUseCase, Depends(new_tcu)],
) -> TagReadModel:
    ...
    fake_tag["user_id"] = new_user_in_db.id
    tag = TagCreateModel.model_validate(fake_tag)

    tag_in_db = tag_command_usecase.create_tag(tag)
    assert tag_in_db is not None
    return tag_in_db


@pytest.fixture
def new_capture_in_db(
    new_user_in_db: UserReadModel,
    fake_capture: dict[str, Any],
    capture_command_usecase: Annotated[CaptureCommandUseCase, Depends(new_tcu)],
) -> CaptureReadModel:
    ...
    fake_capture["user_id"] = new_user_in_db.id
    capture = CaptureCreateModel.model_validate(fake_capture)

    capture_in_db = capture_command_usecase.create_capture(capture)
    assert capture_in_db is not None
    return capture_in_db


def reset_db() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.fixture(scope="function")
def db_fixture() -> Iterator[Session]:
    reset_db()
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture()
async def db_session() -> AsyncIterator[AsyncSession]:
    """Start a test database session."""
    db_name = str(config.db_url).split("/")[-1]
    db_url = str(config.db_url).replace(f"/{db_name}", "/test")

    engine = create_async_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session = async_sessionmaker(engine)()
    yield session
    await session.close()


# def test_user() -> dict[str, str]:
#     return {
#         "id": "1",
#         "email": "matt@bittfurst.xyz",
#         "password": "matt",
#     }


# def test_admin_user() -> dict[str, str]:
#     return {"email": "admin@bittfurst.xyz", "password": "admin"}


@pytest.fixture
async def fastapi_app_async(
    db_session: AsyncSession,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_sync_session] = lambda: db_session
    # application.dependency_overrides[get_current_active_user] = test_user

    return application  # noqa: WPS331


@pytest.fixture()
async def async_client(fastapi_app: FastAPI) -> AsyncIterator[AsyncClient]:
    """Create an http client."""
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        yield client


@pytest.fixture()
def book_query_usecase(db_fixture: Session) -> BookQueryUseCase:
    """Get a book query use case."""
    book_query_service: BookQueryService = BookQueryServiceImpl(db_fixture)
    return BookQueryUseCaseImpl(book_query_service)


@pytest.fixture()
def book_command_usecase(db_fixture: Session) -> BookCommandUseCase:
    book_repository: BookRepository = BookRepositoryImpl(db_fixture)
    uow: BookCommandUseCaseUnitOfWork = BookCommandUseCaseUnitOfWorkImpl(
        db_fixture,
        book_repository=book_repository,
    )
    return BookCommandUseCaseImpl(uow)


@pytest.fixture()
def user_query_usecase(db_fixture: Session) -> UserQueryUseCase:
    """Get a user query use case."""
    user_query_service: UserQueryService = UserQueryServiceImpl(db_fixture)
    return UserQueryUseCaseImpl(user_query_service)


@pytest.fixture()
def user_command_usecase(db_fixture: Session) -> UserCommandUseCase:
    user_repository: UserRepository = UserRepositoryImpl(db_fixture)
    uow: UserCommandUseCaseUnitOfWork = UserCommandUseCaseUnitOfWorkImpl(
        db_fixture,
        user_repository=user_repository,
    )
    return UserCommandUseCaseImpl(uow)


@pytest.fixture()
def tag_query_usecase(db_fixture: Session) -> TagQueryUseCase:
    """Get a tag query use case."""
    tag_query_service: TagQueryService = TagQueryServiceImpl(db_fixture)
    return TagQueryUseCaseImpl(tag_query_service)


@pytest.fixture()
def tag_command_usecase(db_fixture: Session) -> TagCommandUseCase:
    tag_repository: TagRepository = TagRepositoryImpl(db_fixture)
    uow: TagCommandUseCaseUnitOfWork = TagCommandUseCaseUnitOfWorkImpl(
        db_fixture,
        tag_repository=tag_repository,
    )
    return TagCommandUseCaseImpl(uow)


@pytest.fixture()
def capture_query_usecase(db_fixture: Session) -> CaptureQueryUseCase:
    """Get a capture query use case."""
    capture_query_service: CaptureQueryService = CaptureQueryServiceImpl(db_fixture)
    return CaptureQueryUseCaseImpl(capture_query_service)


@pytest.fixture()
def capture_command_usecase(db_fixture: Session) -> CaptureCommandUseCase:
    capture_repository: CaptureRepository = CaptureRepositoryImpl(db_fixture)
    uow: CaptureCommandUseCaseUnitOfWork = CaptureCommandUseCaseUnitOfWorkImpl(
        db_fixture,
        capture_repository=capture_repository,
    )
    return CaptureCommandUseCaseImpl(uow)


@pytest.fixture
def client(
    db_fixture: Session,
    user_query_usecase: UserQueryUseCase,
    user_command_usecase: UserCommandUseCase,
    fake_user: dict[str, Any],
) -> TestClient:
    def _get_db_override() -> Session:
        return db_fixture

    def _get_current_active_user_override() -> UserReadModel:
        try:
            user = user_query_usecase.fetch_users()[0]
        except IndexError:
            logger.debug("Creating a fake user since none exist yet")
            user_model = UserCreateModel.model_validate(fake_user)
            if user_model is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            user = user_command_usecase.create_user(
                user_model,
            )
        return user

    def _get_current_active_super_user_override() -> UserReadModel:
        user = _get_current_active_user_override()
        user.is_superuser = True
        return user

    app = get_app()
    app.dependency_overrides[get_sync_session] = _get_db_override
    app.dependency_overrides[
        get_current_active_super_user
    ] = _get_current_active_super_user_override
    app.dependency_overrides[
        get_current_active_user
    ] = _get_current_active_user_override
    return TestClient(app)

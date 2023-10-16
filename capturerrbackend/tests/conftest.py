from collections.abc import AsyncIterator, Iterator
from datetime import datetime
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from capturerrbackend.app.application import get_app
from capturerrbackend.app.domain.book.book_repository import BookRepository
from capturerrbackend.app.domain.user.user_repository import UserRepository
from capturerrbackend.app.infrastructure.dependencies import get_sync_session
from capturerrbackend.app.infrastructure.sqlite.book import (
    BookCommandUseCaseUnitOfWorkImpl,
    BookQueryServiceImpl,
    BookRepositoryImpl,
)
from capturerrbackend.app.infrastructure.sqlite.database import Base
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
from capturerrbackend.app.usecase.user import (
    UserCommandUseCase,
    UserCommandUseCaseImpl,
    UserCommandUseCaseUnitOfWork,
    UserQueryService,
    UserQueryUseCase,
    UserQueryUseCaseImpl,
)
from capturerrbackend.config.configurator import config  # type: ignore
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
    }


@pytest.fixture
def fake_user() -> dict[str, Any]:
    return {
        "user_name": "matt",
        "first_name": "Matt",
        "last_name": "Bittinger",
        "email": "matt@bittfurst.xyz",
        "created_at": get_int_timestamp(datetime.now()),
        "updated_at": get_int_timestamp(datetime.now()),
        "deleted_at": None,
    }


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


@pytest.fixture
def client(db_fixture: Session) -> TestClient:
    def _get_db_override() -> Session:
        return db_fixture

    app = get_app()
    app.dependency_overrides[get_sync_session] = _get_db_override
    # app.dependency_overrides[get_current_active_user] = test_user
    return TestClient(app)


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


def test_user() -> dict[str, str]:
    return {
        "id": "1",
        "email": "matt@bittfurst.xyz",
        "password": "matt",
    }


def test_admin_user() -> dict[str, str]:
    return {"email": "admin@bittfurst.xyz", "password": "admin"}


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

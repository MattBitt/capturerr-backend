from collections.abc import AsyncIterator, Iterator
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from capturerrbackend.app.domain.book.book_repository import BookRepository
from capturerrbackend.app.infrastructure.sqlite.book import (
    BookCommandUseCaseUnitOfWorkImpl,
    BookRepositoryImpl,
)
from capturerrbackend.app.usecase.book import (
    BookCommandUseCase,
    BookCommandUseCaseImpl,
    BookCommandUseCaseUnitOfWork,
    BookQueryService,
    BookQueryUseCase,
    BookQueryUseCaseImpl,
)

from ..app.application import get_app
from ..app.infrastructure.dependencies import get_sync_session
from ..app.infrastructure.sqlite.book import BookQueryServiceImpl
from ..app.infrastructure.sqlite.database import Base
from ..config.configurator import config  # type: ignore

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

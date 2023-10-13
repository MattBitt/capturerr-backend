from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from capturerrbackend.app.application import get_app
from capturerrbackend.app.services.users import get_current_active_user
from capturerrbackend.app.settings import settings
from capturerrbackend.core.base.model import Base
from capturerrbackend.core.db.dependencies import get_db_session


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Start a test database session."""
    db_name = str(settings.db_url).split("/")[-1]
    db_url = str(settings.db_url).replace(f"/{db_name}", "/test")

    engine = create_async_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session = async_sessionmaker(engine)()
    yield session
    await session.close()


def test_user() -> dict[str, str]:
    return {
        "pk": "1",
        "email": "matt@bittfurst.xyz",
        "password": "matt",
    }


def test_admin_user() -> dict[str, str]:
    return {"email": "admin@bittfurst.xyz", "password": "admin"}


@pytest.fixture
async def fastapi_app(
    db_session: AsyncSession,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: db_session
    application.dependency_overrides[get_current_active_user] = test_user

    return application  # noqa: WPS331


@pytest.fixture()
async def client(fastapi_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an http client."""
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        yield client

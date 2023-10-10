import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from capturerrbackend.app.dao.foo_dao import FooDAO


@pytest.mark.anyio
async def test_creation(
    fastapi_app: FastAPI,
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Tests foo instance creation."""
    url = fastapi_app.url_path_for("create_foo_model")
    test_name = uuid.uuid4().hex
    response = await client.put(
        url,
        json={
            "name": test_name,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    dao = FooDAO(db_session)
    instances = await dao.filter(name=test_name)
    assert instances[0].name == test_name


@pytest.mark.anyio
async def test_getting(
    fastapi_app: FastAPI,
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Tests foo instance retrieval."""
    dao = FooDAO(db_session)
    test_name = uuid.uuid4().hex
    await dao.create_foo_model(name=test_name)
    url = fastapi_app.url_path_for("get_foo_models")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    new_foo = response.json()
    assert new_foo[0]["name"] == test_name
    assert new_foo[0]["pk"] is not None


@pytest.mark.anyio
async def test_add_bar_to_foo(
    fastapi_app: FastAPI,
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Tests foo instance retrieval."""
    dao = FooDAO(db_session)
    test_foo = uuid.uuid4().hex
    test_bar = uuid.uuid4().hex
    await dao.create_foo_model(name=test_foo)
    foo = await dao.filter(name=test_foo)
    assert foo is not None
    assert foo is not []
    assert foo[0].name == test_foo

    url = f"/api/foo/{foo[0].pk}/{test_bar}"
    response = await client.put(url)
    assert response.status_code == status.HTTP_200_OK
    new_foo = response.json()
    assert new_foo["name"] == test_foo
    assert new_foo["pk"] is not None
    assert new_foo["bars"] is not None
    assert new_foo["bars"][0]["title"] == test_bar

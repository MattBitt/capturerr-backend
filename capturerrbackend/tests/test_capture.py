import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from capturerrbackend.db.dao.capture_dao import CaptureDAO


@pytest.mark.anyio
async def test_creation(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests capture instance creation."""
    url = fastapi_app.url_path_for("create_capture_model")
    test_name = uuid.uuid4().hex
    response = await client.put(
        url,
        json={
            "name": test_name,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    dao = CaptureDAO(dbsession)
    instances = await dao.filter(name=test_name)
    assert instances[0].name == test_name


@pytest.mark.anyio
async def test_getting(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests capture instance retrieval."""
    dao = CaptureDAO(dbsession)
    test_name = uuid.uuid4().hex
    await dao.create_capture_model(name=test_name)
    url = fastapi_app.url_path_for("get_capture_models")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    new_capture = response.json()
    assert new_capture[0]["name"] == test_name
    assert new_capture[0]["id"] is not None


@pytest.mark.anyio
async def test_add_tag_to_capture(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests capture instance retrieval."""
    dao = CaptureDAO(dbsession)
    test_capture = uuid.uuid4().hex
    test_tag = uuid.uuid4().hex
    await dao.create_capture_model(name=test_capture)
    capture = await dao.filter(name=test_capture)
    assert capture is not None
    assert capture is not []
    assert capture[0].name == test_capture

    url = f"/api/capture/{capture[0].id}/{test_tag}"
    response = await client.put(url)
    assert response.status_code == status.HTTP_200_OK
    new_capture = response.json()
    assert new_capture["name"] == test_capture
    assert new_capture["id"] is not None
    assert new_capture["tags"] is not None
    assert new_capture["tags"][0]["title"] == test_tag

import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from capturerrbackend.app.dao.tag_dao import TagDAO


@pytest.mark.anyio
async def test_creation(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests tag instance creation."""
    url = fastapi_app.url_path_for("create_tag_model")
    test_title = uuid.uuid4().hex
    response = await client.put(
        url,
        json={
            "title": test_title,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    dao = TagDAO(dbsession)
    instances = await dao.filter(title=test_title)
    assert instances[0].title == test_title


@pytest.mark.anyio
async def test_getting(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests tag instance retrieval."""
    dao = TagDAO(dbsession)
    test_title = uuid.uuid4().hex
    await dao.create_tag_model(title=test_title)
    url = fastapi_app.url_path_for("get_tag_models")
    response = await client.get(url)
    dummies = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(dummies) == 1
    assert dummies[0]["title"] == test_title

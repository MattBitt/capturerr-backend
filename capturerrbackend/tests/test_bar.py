import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from capturerrbackend.app.dao.bar_dao import BarDAO


@pytest.mark.anyio
async def test_creation(
    fastapi_app: FastAPI,
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Tests bar instance creation."""
    url = fastapi_app.url_path_for("create_bar_model")
    test_title = uuid.uuid4().hex
    response = await client.put(
        url,
        json={
            "title": test_title,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    dao = BarDAO(db_session)
    instances = await dao.filter(title=test_title)
    assert instances[0].title == test_title


@pytest.mark.anyio
async def test_getting(
    fastapi_app: FastAPI,
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Tests bar instance retrieval."""
    dao = BarDAO(db_session)
    test_title = uuid.uuid4().hex
    await dao.create_bar_model(title=test_title)
    url = fastapi_app.url_path_for("get_bar_models")
    response = await client.get(url)
    dummies = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(dummies) == 1
    assert dummies[0]["title"] == test_title

import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from capturerrbackend.db.dao.daz_dao import DazDAO


@pytest.mark.anyio
async def test_creation(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests daz instance creation."""
    url = fastapi_app.url_path_for("create_daz_model")
    test_comment = uuid.uuid4().hex
    response = await client.put(
        url,
        json={
            "comment": test_comment,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    dao = DazDAO(dbsession)
    instances = await dao.filter(comment=test_comment)
    assert instances[0].comment == test_comment


@pytest.mark.anyio
async def test_getting(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests daz instance retrieval."""
    dao = DazDAO(dbsession)
    test_comment = uuid.uuid4().hex
    await dao.create_daz_model(comment=test_comment)
    url = fastapi_app.url_path_for("get_daz_models")
    response = await client.get(url)
    dummies = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(dummies) == 1
    assert dummies[0]["comment"] == test_comment

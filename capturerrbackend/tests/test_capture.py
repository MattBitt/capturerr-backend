import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from capturerrbackend.app.schemas.tag import TagSchema
from capturerrbackend.app.services.captures import CaptureService
from capturerrbackend.app.services.tags import TagService


async def create_fake_capture(db: AsyncSession, text: str = "test") -> None:
    """Create a fake capture."""
    service = CaptureService(db)
    await service.add(text=text)


@pytest.mark.anyio
async def test_creation(
    fastapi_app: FastAPI,
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Tests capture instance creation."""
    url = fastapi_app.url_path_for("create_capture")
    test_text = uuid.uuid4().hex
    response = await client.post(
        url,
        json={
            "text": test_text,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    service = CaptureService(db_session)
    instances = await service.get_by_text(text=test_text)
    assert instances.text == test_text


@pytest.mark.anyio
async def test_get_empty_captures(
    fastapi_app: FastAPI,
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Retrieve the Capture instance"""
    url = fastapi_app.url_path_for("get_captures")
    response = await client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_services_create_capture_with_tags(db_session: AsyncSession) -> None:
    t1 = "test-tag1_from_string"
    tag_service = TagService(db_session)
    assert await tag_service.add(t1)
    t1_saved = TagSchema.model_validate(await tag_service.get_tag_by_name(t1))
    cap_service = CaptureService(db_session)
    assert await cap_service.add(text="test", tags=[t1_saved])
    c1 = await cap_service.get_by_text(text="test")
    assert len(c1.tags) == 2
    assert c1.tags[0].name == "test-tag"
    assert c1.tags[1].name == "test-tag2"


# @pytest.mark.anyio
# async def test_get_capture_by_text(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     db_session: AsyncSession,
# ) -> None:
#     test_text = "test"
#     await create_fake_capture(db_session, text=test_text)

#     """Retrieve the Capture instance"""
#     # url = fastapi_app.url_path_for("get_capture_by_text")

#     new_url = f"/api/v2/captures/text/{test_text}"
#     response = await client.get(new_url)
#     dummies = response.json()

#     assert response.status_code == status.HTTP_200_OK
#     assert dummies["text"] == "test"


@pytest.mark.anyio
async def test_capture_service(
    db_session: AsyncSession,
) -> None:
    """Create a Capture instance"""
    service = CaptureService(db_session)
    test_text = "test"
    assert await service.add(text=test_text)
    """Retrieve the Capture instance"""
    capture = await service.get_by_text(text=test_text)
    assert capture.text == test_text


# @pytest.mark.anyio
# async def test_creation(
#     fastapi_app: FastAPI,
#     db_session: AsyncSession,
#     client: AsyncClient,
# ) -> None:
#     """Tests capture instance creation."""
#     url = fastapi_app.url_path_for("create_capture")
#     test_text = uuid.uuid4().hex
#     await client.get("/api/users/me")
#     t1 = await client.post("/api/v2/captures", json={"text": "test_capture"})
#     response = await client.post(
#         url,
#         json={"text": test_text, "captures": [t1.json()["text"]]},
#     )

#     assert response.status_code == status.HTTP_201_CREATED
#     dao = CaptureDAO(db_session)
#     instances = await dao.filter(text=test_text)
#     assert instances[0].text == test_text


# @pytest.mark.anyio
# async def test_getting(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     db_session: AsyncSession,
# ) -> None:
#     """Tests capture instance retrieval."""
#     CaptureDAO(db_session)
#     test_text = uuid.uuid4().hex
#     await client.get("/api/users/me")
#     url = fastapi_app.url_path_for("create_capture")
#     response = await client.post(
#         url,
#         json={"text": test_text, "captures": [1]},
#     )

#     assert response.status_code == status.HTTP_201_CREATED

#     url = fastapi_app.url_path_for("get_captures")
#     response = await client.get(url)
#     assert response.status_code == status.HTTP_200_OK
#     new_capture = response.json()
#     assert new_capture[0]["text"] == test_text
#     assert new_capture[0]["pk"] is not None


# @pytest.mark.anyio
# async def test_add_capture_to_capture(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     db_session: AsyncSession,
# ) -> None:
#     """Tests capture instance retrieval."""
#     dao = CaptureDAO(db_session)
#     test_capture = uuid.uuid4().hex
#     test_capture = uuid.uuid4().hex

#     await dao.create_capture_model(text=test_capture)
#     capture = await dao.filter(text=test_capture)  # type: ignore
#     assert capture is not None
#     assert capture is not []
#     assert capture[0].text == test_capture

#     url = f"/api/capture/{capture[0].pk}/{test_capture}"
#     response = await client.put(url)
#     assert response.status_code == status.HTTP_200_OK
#     new_capture = response.json()
#     assert new_capture["text"] == test_capture
#     assert new_capture["pk"] is not None
#     assert new_capture["captures"] is not None
#     assert new_capture["captures"][0]["title"] == test_capture

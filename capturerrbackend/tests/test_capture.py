# import uuid

# import pytest
# from fastapi import FastAPI
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import AsyncSession
# from starlette import status

# from capturerrbackend.app.services.captures import CaptureService


# async def create_fake_capture(db: AsyncSession, text: str = "test") -> None:
#     """Create a fake capture."""
#     service = CaptureService(db)
#     await service.add(text=text)


# @pytest.mark.anyio
# async def test_creation(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     db_session: AsyncSession,
# ) -> None:
#     """Tests capture instance creation."""
#     url = fastapi_app.url_path_for("create_capture")
#     test_text = uuid.uuid4().hex
#     response = await client.post(
#         url,
#         json={
#             "text": test_text,
#         },
#     )
#     assert response.status_code == status.HTTP_201_CREATED
#     service = CaptureService(db_session)
#     instances = await service.get_by_text(text=test_text)
#     assert instances.text == test_text


# @pytest.mark.anyio
# async def test_get_empty_captures(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     db_session: AsyncSession,
# ) -> None:
#     """Retrieve the Capture instance"""
#     url = fastapi_app.url_path_for("get_captures")
#     response = await client.get(url)
#     assert response.status_code == status.HTTP_404_NOT_FOUND


# # @pytest.mark.anyio
# # async def test_services_create_capture_with_tags(db_session: AsyncSession) -> None:
# #     t1 = "test-tag1_from_string"
# #     tag_service = TagService(db_session)
# #     assert await tag_service.add(t1)
# #     t1_saved = TagSchema.model_validate(await tag_service.get_tag_by_name(t1))
# #     cap_service = CaptureService(db_session)
# #     assert await cap_service.add(text="test")
# #     c1 = await cap_service.get_by_text(text="test")

# #     assert len(c1.tags) == 2
# #     assert c1.tags[0].name == "test-tag"
# #     assert c1.tags[1].name == "test-tag2"


# @pytest.mark.anyio
# async def test_capture_service(
#     db_session: AsyncSession,
# ) -> None:
#     """Create a Capture instance"""
#     service = CaptureService(db_session)
#     test_text = "test"
#     assert await service.add(text=test_text)
#     """Retrieve the Capture instance"""
#     capture = await service.get_by_text(text=test_text)
#     assert capture.text == test_text

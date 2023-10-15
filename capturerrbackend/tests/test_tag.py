# import uuid

# import pytest
# from fastapi import FastAPI
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import AsyncSession
# from starlette import status

# from capturerrbackend.app.services.tags import TagService


# async def create_fake_tag(db: AsyncSession, name: str = "test") -> None:
#     """Create a fake tag."""
#     service = TagService(db)
#     await service.add(name=name)


# @pytest.mark.anyio
# async def test_creation(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     db_session: AsyncSession,
# ) -> None:
#     """Tests tag instance creation."""
#     url = fastapi_app.url_path_for("create_tag")
#     test_name = uuid.uuid4().hex
#     response = await client.post(
#         url,
#         json={
#             "name": test_name,
#         },
#     )
#     assert response.status_code == status.HTTP_201_CREATED
#     service = TagService(db_session)
#     instances = await service.get_tag_by_name(name=test_name)
#     assert instances.name == test_name


# # @pytest.mark.anyio
# # async def test_getting(
# #     fastapi_app: FastAPI,
# #     client: AsyncClient,
# #     db_session: AsyncSession,
# # ) -> None:
# #     """Tests tag instance retrieval."""
# #     dao = TagDAO(db_session)
# #     test_name = uuid.uuid4().hex
# #     await dao.create_tag_model(name=test_name)
# #     url = fastapi_app.url_path_for("get_tags")
# #     response = await client.get(url)
# #     dummies = response.json()

# #     assert response.status_code == status.HTTP_200_OK
# #     assert len(dummies) == 1
# #     assert dummies[0]["name"] == test_name


# @pytest.mark.anyio
# async def test_get_empty_tags(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     db_session: AsyncSession,
# ) -> None:
#     """Retrieve the Tag instance"""
#     url = fastapi_app.url_path_for("get_tags")
#     response = await client.get(url)
#     assert response.status_code == status.HTTP_404_NOT_FOUND


# @pytest.mark.anyio
# async def test_get_tag_by_name(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     db_session: AsyncSession,
# ) -> None:
#     test_name = "test"
#     await create_fake_tag(db_session, name=test_name)

#     """Retrieve the Tag instance"""
#     # url = fastapi_app.url_path_for("get_tag_by_name")

#     new_url = f"/api/v2/tags/name/{test_name}"
#     response = await client.get(new_url)
#     dummies = response.json()

#     assert response.status_code == status.HTTP_200_OK
#     assert dummies["name"] == "test"


# @pytest.mark.anyio
# async def test_tag_service(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     db_session: AsyncSession,
# ) -> None:
#     """Create a Tag instance"""
#     service = TagService(db_session)
#     test_name = "test"
#     assert await service.add(name=test_name)
#     """Retrieve the Tag instance"""
#     tag = await service.get_tag_by_name(name=test_name)
#     assert tag.name == test_name

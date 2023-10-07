# # type: ignore
# import uuid

# import pytest
# from fastapi import FastAPI
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import AsyncSession
# from starlette import status


# @pytest.mark.anyio
# async def test_login(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     dbsession: AsyncSession,
# ) -> None:
#     """Tests auth instance creation."""
#     url = fastapi_app.url_path_for("create_auth_model")

#     response = await client.put(
#         url,
#         json={
#             "title": test_title,
#         },
#     )
#     assert response.status_code == status.HTTP_200_OK
#     dao = AuthDAO(dbsession)
#     instances = await dao.filter(title=test_title)
#     assert instances[0].title == test_title


# @pytest.mark.anyio
# async def test_getting(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     dbsession: AsyncSession,
# ) -> None:
#     """Tests auth instance retrieval."""
#     dao = AuthDAO(dbsession)
#     test_title = uuid.uuid4().hex
#     await dao.create_auth_model(title=test_title)
#     url = fastapi_app.url_path_for("get_auth_models")
#     response = await client.get(url)
#     dummies = response.json()

#     assert response.status_code == status.HTTP_200_OK
#     assert len(dummies) == 1
#     assert dummies[0]["title"] == test_title

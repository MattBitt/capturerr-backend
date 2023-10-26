from typing import Any

import pytest
from fastapi.testclient import TestClient

from capturerrbackend.app.domain.tag.tag_exception import (
    TagAlreadyExistsError,
    TagNotFoundError,
    TagsNotFoundError,
)
from capturerrbackend.app.usecase.tag import TagReadModel
from capturerrbackend.app.usecase.user import UserReadModel


def test_create_tag(
    client: TestClient,
    new_user_in_db: UserReadModel,
    fake_tag: dict[str, Any],
) -> None:
    # Arrange

    # Act
    fake_tag["user_id"] = new_user_in_db.id
    response = client.post("/api/me/tags", json=fake_tag)

    # Assert
    assert response.status_code == 201
    assert response.json()["text"] == fake_tag["text"]


def test_create_tag_with_existing_text(
    client: TestClient,
    fake_tag: dict[str, Any],
) -> None:
    # Arrange

    # Act
    response = client.post("/api/me/tags", json=fake_tag)
    assert response.status_code == 201

    response = client.post("/api/me/tags", json=fake_tag)
    assert response.status_code == 409
    assert response.json()["detail"] == TagAlreadyExistsError.detail


def test_get_tags(client: TestClient, fake_tag: dict[str, Any]) -> None:
    # Arrange
    response = client.post("/api/me/tags", json=fake_tag)
    assert response.status_code == 201
    # Act
    response = client.get("/api/me/tags")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_tags_with_no_tags(client: TestClient) -> None:
    # Arrange

    # Act
    response = client.get("/api/me/tags")
    assert response.status_code == TagsNotFoundError.status_code
    assert response.json()["detail"] == TagsNotFoundError.detail


def test_get_tag(client: TestClient, new_tag_in_db: TagReadModel) -> None:
    # Arrange
    tag_id = new_tag_in_db.id

    # Act
    response = client.get(f"/api/me/tags/{tag_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == tag_id


def test_get_tag_with_invalid_id(client: TestClient) -> None:
    # Arrange
    tag_id = 999

    # Act
    response = client.get(f"/api/me/tags/{tag_id}")
    # Assert
    assert response.status_code == TagNotFoundError.status_code
    assert response.json()["detail"] == TagNotFoundError.detail


def test_update_tag(
    client: TestClient,
    new_tag_in_db: TagReadModel,
) -> None:
    # Arrange
    tag_id = new_tag_in_db.id
    data = new_tag_in_db.model_dump()
    data["entry"] = "Updated Test Tag"
    data["notes"] = "Updated Test Notes"
    data["entry_type"] = "updated entry type"
    # Act
    response = client.put(f"/api/me/tags/{tag_id}", json=data)

    # Assert
    assert response.status_code == 202
    assert response.json()["id"] == tag_id
    assert response.json()["text"] == data["text"]


def test_update_tag_with_invalid_id(
    client: TestClient,
    new_tag_in_db: TagReadModel,
) -> None:
    # Arrange
    tag_id = "some invalid id"
    data = new_tag_in_db.model_dump()
    data["text"] = "Updated Test Tag"

    # Act
    response = client.put(f"/api/me/tags/{tag_id}", json=data)
    assert response.status_code == TagNotFoundError.status_code
    assert response.json()["detail"] == TagNotFoundError.detail


def test_delete_tag(client: TestClient, fake_tag: dict[str, Any]) -> None:
    # Arrange
    response = client.post("/api/me/tags", json=fake_tag)
    assert response.status_code == 201
    tag_id = response.json()["id"]

    # Act
    response = client.delete(f"/api/me/tags/{tag_id}")

    # Assert
    assert response.status_code == 202

    tags = client.get("/api/me/tags")
    assert tags.status_code == 404


@pytest.mark.anyio
def test_delete_tag_with_invalid_id(client: TestClient) -> None:
    # Arrange
    tag_id = 999

    # Act
    try:
        client.delete(f"/api/me/tags/{tag_id}")
    except TagNotFoundError as err:
        # Assert
        assert err.status_code == TagNotFoundError.status_code
        assert err.detail == TagNotFoundError.detail


# def test_create_tag(client: TestClient, new_user_in_db,
# fake_tag: dict[str, Any]) -> None:
#     # Arrange

#     # Act
#     response = client.post("/api/me/tags", json=fake_tag)

#     # Assert
#     assert response.status_code == 201
#     assert response.json()["text"] == fake_tag["text"]


# def test_create_tag_with_existing_text(
#     client: TestClient,
#     fake_tag: dict[str, Any],
# ) -> None:
#     # Arrange

#     # Act
#     response = client.post("/api/tags", json=fake_tag)
#     assert response.status_code == 201

#     response = client.post("/api/tags", json=fake_tag)
#     assert response.status_code == 409
#     assert response.json()["detail"] == TagAlreadyExistsError.detail


# def test_get_tags(client: TestClient, fake_tag: dict[str, Any]) -> None:
#     # Arrange
#     response = client.post("/api/tags", json=fake_tag)
#     assert response.status_code == 201
#     # Act
#     response = client.get("/api/tags")

#     # Assert
#     assert response.status_code == 200
#     assert len(response.json()) > 0


# def test_get_tags_with_no_tags(client: TestClient) -> None:
#     # Arrange

#     # Act
#     response = client.get("/api/tags")
#     assert response.status_code == TagsNotFoundError.status_code
#     assert response.json()["detail"] == TagsNotFoundError.detail


# def test_get_tag(client: TestClient, fake_tag: dict[str, Any]) -> None:
#     # Arrange
#     response = client.post("/api/tags", json=fake_tag)
#     assert response.status_code == 201
#     tag_id = response.json()["id"]

#     # Act
#     response = client.get(f"/api/tags/{tag_id}")

#     # Assert
#     assert response.status_code == 200
#     assert response.json()["id"] == tag_id


# def test_get_tag_with_invalid_id(client: TestClient) -> None:
#     # Arrange
#     tag_id = 999

#     # Act
#     response = client.get(f"/api/tags/{tag_id}")
#     # Assert
#     assert response.status_code == TagNotFoundError.status_code
#     assert response.json()["detail"] == TagNotFoundError.detail


# def test_update_tag(client: TestClient, fake_tag: dict[str, Any]) -> None:
#     # Arrange
#     response = client.post("/api/tags", json=fake_tag)
#     assert response.status_code == 201

#     tag_id = response.json()["id"]
#     data = {
#         "text": "updated-tag",
#     }
#     # Act
#     response = client.put(f"/api/tags/{tag_id}", json=data)

#     # Assert
#     assert response.status_code == 202
#     assert response.json()["id"] == tag_id
#     assert response.json()["text"] == data["text"]


# def test_update_tag_with_invalid_id(
#     client: TestClient,
#     fake_tag: dict[str, Any],
# ) -> None:
#     # Arrange
#     response = client.post("/api/tags", json=fake_tag)
#     assert response.status_code == 201

#     tag_id = 999
#     data = {
#         "text": "Updated Test Tag",
#         "isbn": "0987658521",
#         "page": 300,
#         "read_page": 86,
#         "user_id": "vytxeTZskVKR7C7WgdSP3d",
#     }
#     # Act
#     response = client.put(f"/api/tags/{tag_id}", json=data)
#     assert response.status_code == TagNotFoundError.status_code
#     assert response.json()["detail"] == TagNotFoundError.detail


# def test_delete_tag(client: TestClient, fake_tag: dict[str, Any]) -> None:
#     # Arrange
#     response = client.post("/api/tags", json=fake_tag)
#     assert response.status_code == 201
#     tag_id = response.json()["id"]

#     # Act
#     response = client.delete(f"/api/tags/{tag_id}")

#     # Assert
#     assert response.status_code == 202

#     tags = client.get("/api/tags")
#     assert tags.status_code == 404


# @pytest.mark.anyio
# def test_delete_tag_with_invalid_id(client: TestClient) -> None:
#     # Arrange
#     tag_id = 999

#     # Act
#     try:
#         client.delete(f"/api/tags/{tag_id}")
#     except TagNotFoundError as err:
#         # Assert
#         assert err.status_code == TagNotFoundError.status_code
#         assert err.detail == TagNotFoundError.detail

from typing import Any

import pytest
from fastapi.testclient import TestClient

from capturerrbackend.app.domain.user.user_exception import (
    UserAlreadyExistsError,
    UserNotFoundError,
)

# app = FastAPI()
# client = TestClient(app)


def test_create_user(client: TestClient, fake_user: dict[str, Any]) -> None:
    # Arrange

    # Act
    response = client.post("/api/users", json=fake_user)

    # Assert
    assert response.status_code == 201
    # assert response.json()["user_name"] == data["user_name"]
    # assert response.json()["first_name"] == data["first_name"]
    # assert response.json()["isbn"] == data["isbn"]
    # assert response.json()["last_name"] == data["last_name"]
    # assert response.json()["email"] == data["email"]


def test_create_user_with_existing_user_name(
    client: TestClient,
    fake_user: dict[str, Any],
) -> None:
    # Arrange
    response = client.post("/api/users", json=fake_user)
    assert response.status_code == 201

    # Act
    response = client.post("/api/users", json=fake_user)

    # Assert
    assert response.status_code == 409
    assert response.json()["detail"] == UserAlreadyExistsError.message


def test_get_users(client: TestClient, fake_user: dict[str, Any]) -> None:
    # Arrange
    response = client.post("/api/users", json=fake_user)
    assert response.status_code == 201
    # Act
    response = client.get("/api/users")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_users_with_no_users(client: TestClient) -> None:
    # Arrange

    # Act
    response = client.get("/users")

    # Assert
    assert response.status_code == 404
    # assert response.json()["detail"] == UsersNotFoundError.message


def test_get_user(client: TestClient, fake_user: dict[str, Any]) -> None:
    # Arrange
    response = client.post("/api/users", json=fake_user)
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Act
    response = client.get(f"/api/users/{user_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_get_user_with_invalid_id(client: TestClient) -> None:
    # Arrange
    user_id = 999

    # Act
    response = client.get(f"/api/users/{user_id}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == UserNotFoundError.message


def test_update_user(client: TestClient, fake_user: dict[str, Any]) -> None:
    # Arrange
    response = client.post("/api/users", json=fake_user)
    assert response.status_code == 201

    user_id = response.json()["id"]
    data = {
        "user_name": "Updated Test User",
        "last_name": "Bitt",
        "first_name": "Matt",
        "email": "matt@bittfurst.xyz",
    }
    # Act
    response = client.put(f"/api/users/{user_id}", json=data)

    # Assert
    assert response.status_code == 202
    assert response.json()["id"] == user_id
    assert response.json()["user_name"] == data["user_name"]
    assert response.json()["email"] == data["email"]
    assert response.json()["last_name"] == data["last_name"]
    assert response.json()["first_name"] == data["first_name"]


def test_update_user_with_invalid_id(
    client: TestClient,
    fake_user: dict[str, Any],
) -> None:
    # Arrange
    response = client.post("/api/users", json=fake_user)
    assert response.status_code == 201

    user_id = 999
    data = {
        "user_name": "Updated Test User",
        "email": "matt@bittfurst.xyz",
        "last_name": "bizzle",
        "first_name": "mizzle",
    }
    # Act
    response = client.put(f"/api/users/{user_id}", json=data)

    # Assert
    assert response.status_code == 404
    # assert response.json()["detail"] == UserNotFoundError.message


def test_delete_user(client: TestClient, fake_user: dict[str, Any]) -> None:
    # Arrange
    response = client.post("/api/users", json=fake_user)
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Act
    response = client.delete(f"/api/users/{user_id}")

    # Assert
    assert response.status_code == 202

    users = client.get("/api/users")
    assert users.status_code == 404


@pytest.mark.anyio
def test_delete_user_with_invalid_id(client: TestClient) -> None:
    # Arrange
    user_id = 999

    # Act
    response = client.delete(f"/api/users/{user_id}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == UserNotFoundError.message

from typing import Any

from fastapi.testclient import TestClient

from capturerrbackend.app.domain.user.user_exception import (
    UserNameAlreadyExistsError,
    UserNotFoundError,
)
from capturerrbackend.app.usecase.book import BookReadModel
from capturerrbackend.app.usecase.user import UserReadModel

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
    new_user_in_db: UserReadModel,
) -> None:
    # Arrange

    # Act
    response = client.post("/api/users", json=fake_user)

    # Assert
    assert response.status_code == 409
    assert response.json()["detail"] == UserNameAlreadyExistsError.detail


def test_get_users(client: TestClient, new_user_in_db: UserReadModel) -> None:
    # Arrange

    # Act
    response = client.get("/api/users")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["id"] == new_user_in_db.id


def test_get_users_with_no_users(client: TestClient) -> None:
    # Arrange

    # Act
    response = client.get("/users")

    # Assert
    assert response.status_code == 404
    # assert response.json()["detail"] == UsersNotFoundError.message


def test_get_user(client: TestClient, new_user_in_db: UserReadModel) -> None:
    # Arrange

    user_id = new_user_in_db.id

    # Act
    response = client.get(f"/api/users/{user_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_get_user_with_book(
    client: TestClient,
    new_user_in_db: UserReadModel,
    new_book_in_db: BookReadModel,
) -> None:
    # Arrange

    user_id = new_user_in_db.id

    # Act
    response = client.get(f"/api/users/{user_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert response.json()["books"][0]["id"] == new_book_in_db.id


def test_get_user_with_invalid_id(client: TestClient) -> None:
    # Arrange
    user_id = 999

    # Act
    response = client.get(f"/api/users/{user_id}")

    # Assert
    # TODO How do I know if a bad id is
    assert response.status_code == UserNotFoundError.status_code
    assert response.json()["detail"] == UserNotFoundError.detail


def test_update_user(client: TestClient, new_user_in_db: UserReadModel) -> None:
    # Arrange
    user_id = new_user_in_db.id
    data = {
        "user_name": "matt",
        "last_name": "Bizzle",
        "first_name": "Matt",
        "email": "matt@bittfurst.xyz",
    }

    # Act
    response = client.put(f"/api/users/{user_id}", json=data)

    # Assert
    assert response.status_code == 202

    # assert response.json()["updated_at"] > original_updated_at

    assert response.json()["id"] == user_id
    assert response.json()["user_name"] == data["user_name"]
    assert response.json()["email"] == data["email"]
    assert response.json()["last_name"] == data["last_name"]
    assert response.json()["first_name"] == data["first_name"]


def test_update_user_with_invalid_id(
    client: TestClient,
    new_user_in_db: UserReadModel,
) -> None:
    # Arrange

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
    assert response.status_code == UserNotFoundError.status_code
    assert response.json()["detail"] == UserNotFoundError.detail


def test_delete_user(client: TestClient, new_user_in_db: UserReadModel) -> None:
    # Arrange
    user_id = new_user_in_db.id

    # Act
    response = client.delete(f"/api/users/{user_id}")

    # Assert
    assert response.status_code == 202

    users = client.get("/api/users")
    assert users.status_code == 200
    assert users.json()[0]["id"] == user_id
    assert users.json()[0]["deleted_at"] is not None


def test_delete_user_with_invalid_id(client: TestClient) -> None:
    # Arrange
    user_id = 999

    # Act
    response = client.delete(f"/api/users/{user_id}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == UserNotFoundError.detail


def test_login_user(client: TestClient, new_user_in_db: UserReadModel) -> None:
    # Arrange

    # Act
    data = {
        "user_name": new_user_in_db.user_name,
        "password": "matt",
    }
    response = client.post("/api/users/login", json=data)

    # Assert
    assert response.status_code == 200
    assert len(response.json()) > 0

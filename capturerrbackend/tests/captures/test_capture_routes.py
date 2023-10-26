from typing import Any

import pytest
from fastapi.testclient import TestClient

from capturerrbackend.app.domain.capture.capture_exception import (
    CaptureAlreadyExistsError,
    CaptureNotFoundError,
    CapturesNotFoundError,
)
from capturerrbackend.app.usecase.capture import CaptureReadModel
from capturerrbackend.app.usecase.user import UserReadModel

# app = FastAPI()
# client = TestClient(app)


def test_create_capture(
    client: TestClient,
    new_user_in_db: UserReadModel,
    fake_capture: dict[str, Any],
) -> None:
    # Arrange

    # Act
    fake_capture["user_id"] = new_user_in_db.id
    response = client.post("/api/me/captures", json=fake_capture)

    # Assert
    assert response.status_code == 201
    assert response.json()["entry"] == fake_capture["entry"]


def test_create_capture_with_existing_text(
    client: TestClient,
    fake_capture: dict[str, Any],
) -> None:
    # Arrange

    # Act
    response = client.post("/api/me/captures", json=fake_capture)
    assert response.status_code == 201

    response = client.post("/api/me/captures", json=fake_capture)
    assert response.status_code == 409
    assert response.json()["detail"] == CaptureAlreadyExistsError.detail


def test_get_captures(client: TestClient, fake_capture: dict[str, Any]) -> None:
    # Arrange
    response = client.post("/api/me/captures", json=fake_capture)
    assert response.status_code == 201
    # Act
    response = client.get("/api/me/captures")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_captures_with_no_captures(client: TestClient) -> None:
    # Arrange

    # Act
    response = client.get("/api/me/captures")
    assert response.status_code == CapturesNotFoundError.status_code
    assert response.json()["detail"] == CapturesNotFoundError.detail


def test_get_capture(client: TestClient, new_capture_in_db: CaptureReadModel) -> None:
    # Arrange
    capture_id = new_capture_in_db.id

    # Act
    response = client.get(f"/api/me/captures/{capture_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == capture_id


def test_get_capture_with_invalid_id(client: TestClient) -> None:
    # Arrange
    capture_id = 999

    # Act
    response = client.get(f"/api/me/captures/{capture_id}")
    # Assert
    assert response.status_code == CaptureNotFoundError.status_code
    assert response.json()["detail"] == CaptureNotFoundError.detail


def test_update_capture(
    client: TestClient,
    new_capture_in_db: CaptureReadModel,
) -> None:
    # Arrange
    capture_id = new_capture_in_db.id
    data = new_capture_in_db.model_dump()
    data["entry"] = "Updated Test Capture"
    data["notes"] = "Updated Test Notes"
    data["entry_type"] = "updated entry type"
    # Act
    response = client.put(f"/api/me/captures/{capture_id}", json=data)

    # Assert
    assert response.status_code == 202
    assert response.json()["id"] == capture_id
    assert response.json()["entry"] == data["entry"]


def test_update_capture_with_invalid_id(
    client: TestClient,
    new_capture_in_db: CaptureReadModel,
) -> None:
    # Arrange
    capture_id = "some invalid id"
    data = new_capture_in_db.model_dump()
    data["entry"] = "Updated Test Capture"
    data["notes"] = "Updated Test Notes"
    data["entry_type"] = "updated entry type"

    # Act
    response = client.put(f"/api/me/captures/{capture_id}", json=data)
    assert response.status_code == CaptureNotFoundError.status_code
    assert response.json()["detail"] == CaptureNotFoundError.detail


def test_delete_capture(client: TestClient, fake_capture: dict[str, Any]) -> None:
    # Arrange
    response = client.post("/api/me/captures", json=fake_capture)
    assert response.status_code == 201
    capture_id = response.json()["id"]

    # Act
    response = client.delete(f"/api/me/captures/{capture_id}")

    # Assert
    assert response.status_code == 202

    captures = client.get("/api/me/captures")
    assert captures.status_code == 404


@pytest.mark.anyio
def test_delete_capture_with_invalid_id(client: TestClient) -> None:
    # Arrange
    capture_id = 999

    # Act
    try:
        client.delete(f"/api/me/captures/{capture_id}")
    except CaptureNotFoundError as err:
        # Assert
        assert err.status_code == CaptureNotFoundError.status_code
        assert err.detail == CaptureNotFoundError.detail

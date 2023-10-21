from typing import Any

from fastapi.testclient import TestClient


def test_route_handler_422(client: TestClient, fake_book: dict[str, Any]) -> None:
    # fake_user.pop("user_name")
    response = client.post("/api/users", json=fake_book)
    assert response.status_code == 422
    assert response.json()["error"] == "Validation Error"

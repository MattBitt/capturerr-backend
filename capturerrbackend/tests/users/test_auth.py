from typing import Any

from fastapi.testclient import TestClient

from capturerrbackend.app.infrastructure.dependencies import get_current_user
from capturerrbackend.app.usecase.user.user_auth_service import (
    Token,
    create_access_token,
    get_password_hash,
    verify_password,
)
from capturerrbackend.app.usecase.user.user_query_usecase import UserQueryUseCaseImpl


def test_hash_password() -> None:
    password = "matt"
    hashed_password = get_password_hash(password)
    assert hashed_password != password
    assert verify_password(password, hashed_password) is True


def test_verify_token_access() -> None:
    ...


def test_get_current_user(
    client: TestClient,
    fake_user: dict[str, Any],
    user_query_usecase: UserQueryUseCaseImpl,
) -> None:
    response = client.post("/api/users", json=fake_user)

    # Assert
    assert response.status_code == 201
    token = Token(access_token=create_access_token(fake_user), token_type="bearer")
    user = get_current_user(token=token.access_token, user_query=user_query_usecase)
    assert user.user_name == fake_user["user_name"]

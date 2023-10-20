from typing import Any

import pytest
from fastapi.testclient import TestClient

from capturerrbackend.app.domain.book.book_exception import (
    BookIsbnAlreadyExistsError,
    BookNotFoundError,
    BooksNotFoundError,
)

# app = FastAPI()
# client = TestClient(app)


def test_create_book(client: TestClient) -> None:
    # Arrange
    data = {
        "title": "Test Book",
        "read_page": 60,
        "isbn": "978-1-445-01022-1",
        "page": 100,
        "user_id": "vytxeTZskVKR7C7WgdSP3d",
    }

    # Act
    response = client.post("/api/books", json=data)

    # Assert
    assert response.status_code == 201
    # assert response.json()["title"] == data["title"]
    # assert response.json()["read_page"] == data["read_page"]
    # assert response.json()["isbn"] == data["isbn"]
    # assert response.json()["page"] == data["page"]


def test_create_book_with_existing_isbn(
    client: TestClient,
    fake_book: dict[str, Any],
) -> None:
    # Arrange

    # Act
    response = client.post("/api/books", json=fake_book)
    assert response.status_code == 201

    response = client.post("/api/books", json=fake_book)
    assert response.status_code == 409
    assert response.json()["detail"] == BookIsbnAlreadyExistsError.detail


def test_get_books(client: TestClient, fake_book: dict[str, Any]) -> None:
    # Arrange
    response = client.post("/api/books", json=fake_book)
    assert response.status_code == 201
    # Act
    response = client.get("/api/books")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_books_with_no_books(client: TestClient) -> None:
    # Arrange

    # Act
    response = client.get("/api/books")
    assert response.status_code == BooksNotFoundError.status_code
    assert response.json()["detail"] == BooksNotFoundError.detail


def test_get_book(client: TestClient, fake_book: dict[str, Any]) -> None:
    # Arrange
    response = client.post("/api/books", json=fake_book)
    assert response.status_code == 201
    book_id = response.json()["id"]

    # Act
    response = client.get(f"/api/books/{book_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == book_id


def test_get_book_with_invalid_id(client: TestClient) -> None:
    # Arrange
    book_id = 999

    # Act
    response = client.get(f"/api/books/{book_id}")
    # Assert
    assert response.status_code == BookNotFoundError.status_code
    assert response.json()["detail"] == BookNotFoundError.detail


def test_update_book(client: TestClient, fake_book: dict[str, Any]) -> None:
    # Arrange
    response = client.post("/api/books", json=fake_book)
    assert response.status_code == 201

    book_id = response.json()["id"]
    data = {
        "title": "Updated Test Book",
        "isbn": "978-0-545-01022-1",
        "page": 123,
        "read_page": 86,
        "user_id": "vytxeTZskVKR7C7WgdSP3d",
    }
    # Act
    response = client.put(f"/api/books/{book_id}", json=data)

    # Assert
    assert response.status_code == 202
    assert response.json()["id"] == book_id
    assert response.json()["title"] == data["title"]
    assert response.json()["isbn"] == data["isbn"]
    assert response.json()["page"] == data["page"]
    assert response.json()["read_page"] == data["read_page"]


def test_update_book_with_invalid_id(
    client: TestClient,
    fake_book: dict[str, Any],
) -> None:
    # Arrange
    response = client.post("/api/books", json=fake_book)
    assert response.status_code == 201

    book_id = 999
    data = {
        "title": "Updated Test Book",
        "isbn": "0987658521",
        "page": 300,
        "read_page": 86,
        "user_id": "vytxeTZskVKR7C7WgdSP3d",
    }
    # Act
    response = client.put(f"/api/books/{book_id}", json=data)
    assert response.status_code == BookNotFoundError.status_code
    assert response.json()["detail"] == BookNotFoundError.detail


def test_delete_book(client: TestClient, fake_book: dict[str, Any]) -> None:
    # Arrange
    response = client.post("/api/books", json=fake_book)
    assert response.status_code == 201
    book_id = response.json()["id"]

    # Act
    response = client.delete(f"/api/books/{book_id}")

    # Assert
    assert response.status_code == 202

    books = client.get("/api/books")
    assert books.status_code == 404


@pytest.mark.anyio
def test_delete_book_with_invalid_id(client: TestClient) -> None:
    # Arrange
    book_id = 999

    # Act
    try:
        client.delete(f"/api/books/{book_id}")
    except BookNotFoundError as err:
        # Assert
        assert err.status_code == BookNotFoundError.status_code
        assert err.detail == BookNotFoundError.detail

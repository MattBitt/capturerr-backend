import pytest
import json
from fastapi.testclient import TestClient
from capturerrbackend.app.domain.book.book_exception import (
    BookIsbnAlreadyExistsError,
    BookNotFoundError,
    BooksNotFoundError,
)
from fastapi import FastAPI
from httpx import AsyncClient

# app = FastAPI()
# client = TestClient(app)


@pytest.mark.anyio
async def test_create_book(client: AsyncClient) -> None:
    # Arrange
    data = {
        "title": "Test Book",
        "read_page": 60,
        "isbn": "978-1-445-01022-1",
        "page": 100,
    }

    # Act
    response = await client.post("/api/books", json=data)

    # Assert
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]
    assert response.json()["read_page"] == data["read_page"]
    assert response.json()["isbn"] == data["isbn"]
    assert response.json()["page"] == data["page"]


@pytest.mark.anyio
async def test_create_book_with_existing_isbn(client: AsyncClient) -> None:
    # Arrange
    data = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "978-1-445-01022-1",
        "description": "Test Description",
    }

    # Act
    response = await client.post("/books", json=data)

    # Assert
    assert response.status_code == 409
    assert response.json()["detail"] == BookIsbnAlreadyExistsError.message


@pytest.mark.anyio
async def test_get_books(client: AsyncClient):
    # Arrange

    # Act
    response = await client.get("/books")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.anyio
async def test_get_books_with_no_books(client: AsyncClient):
    # Arrange

    # Act
    response = await client.get("/books")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == BooksNotFoundError.message


@pytest.mark.anyio
async def test_get_book(client: AsyncClient) -> None:
    # Arrange
    book_id = 1

    # Act
    response = await client.get(f"/books/{book_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == book_id


@pytest.mark.anyio
async def test_get_book_with_invalid_id(client: AsyncClient):
    # Arrange
    book_id = 999

    # Act
    response = await client.get(f"/books/{book_id}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == BookNotFoundError.message


@pytest.mark.anyio
async def test_update_book(client: AsyncClient) -> None:
    # Arrange
    book_id = 1
    data = {
        "title": "Updated Test Book",
        "author": "Updated Test Author",
        "isbn": "0987654321",
        "description": "Updated Test Description",
    }

    # Act
    response = await client.put(f"/books/{book_id}", json=data)

    # Assert
    assert response.status_code == 202
    assert response.json()["id"] == book_id
    assert response.json()["title"] == data["title"]
    assert response.json()["author"] == data["author"]
    assert response.json()["isbn"] == data["isbn"]
    assert response.json()["description"] == data["description"]


@pytest.mark.anyio
async def test_update_book_with_invalid_id(client: AsyncClient) -> None:
    # Arrange
    book_id = 999
    data = {
        "title": "Updated Test Book",
        "author": "Updated Test Author",
        "isbn": "0987654321",
        "description": "Updated Test Description",
    }

    # Act
    response = await client.put(f"/books/{book_id}", json=data)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == BookNotFoundError.message


@pytest.mark.anyio
async def test_delete_book(client: AsyncClient) -> None:
    # Arrange
    book_id = 1

    # Act
    response = await client.delete(f"/books/{book_id}")

    # Assert
    assert response.status_code == 202


@pytest.mark.anyio
async def test_delete_book_with_invalid_id(client: AsyncClient) -> None:
    # Arrange
    book_id = 999

    # Act
    response = await client.delete(f"/books/{book_id}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == BookNotFoundError.message

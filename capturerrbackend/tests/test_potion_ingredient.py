import pytest
from fastapi import status


@pytest.mark.anyio
async def test_create_ingredient(client) -> None:  # type: ignore
    response = await client.post("/api/v2/ingredients", json={"name": "Carrot"})
    assert response.status_code == status.HTTP_201_CREATED
    pk = response.json().get("pk")
    assert pk is not None

    response = await client.get("/api/v2/ingredients")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["pk"] == pk


@pytest.mark.anyio
async def test_list_ingredients(client) -> None:  # type: ignore
    for n in range(3):
        await client.post("/api/v2/ingredients", json={"name": str(n)})

    response = await client.get("/api/v2/ingredients")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


@pytest.mark.anyio
async def test_get_ingredient(client) -> None:  # type: ignore
    response = await client.post("/api/v2/ingredients", json={"name": "Sugar"})
    assert response.status_code == status.HTTP_201_CREATED
    pk = response.json()["pk"]
    assert pk is not None

    response = await client.get(f"/api/v2/ingredients/{pk}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["pk"] == pk


@pytest.mark.anyio
async def test_create_potion(client) -> None:  # type: ignore
    response = await client.post("/api/v2/ingredients", json={"name": "Sugar"})

    response = await client.post(
        "/api/v2/potions",
        json={
            "name": "Potion of Swiftness",
            "ingredients": [response.json()["pk"]],
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    pk = response.json().get("pk")
    assert pk is not None

    response = await client.get("/api/v2/potions")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["pk"] == pk
    assert response.json()[0]["ingredients"][0]["name"] == "Sugar"


@pytest.mark.anyio
async def test_list_potions(client) -> None:  # type: ignore
    response = await client.post("/api/v2/ingredients", json={"name": "Sugar"})
    ingredient_pk = response.json()["pk"]

    for n in range(3):
        await client.post(
            "/api/v2/potions",
            json={"name": str(n), "ingredients": [ingredient_pk]},
        )

    response = await client.get("/api/v2/potions")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


@pytest.mark.anyio
async def test_get_potion(client) -> None:  # type: ignore
    response = await client.post("/api/v2/ingredients", json={"name": "Sugar"})

    response = await client.post(
        "/api/v2/potions",
        json={
            "name": "Potion of Swiftness",
            "ingredients": [response.json()["pk"]],
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    pk = response.json().get("pk")
    assert pk is not None

    response = await client.get(f"/api/v2/potions/{pk}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["pk"] == pk

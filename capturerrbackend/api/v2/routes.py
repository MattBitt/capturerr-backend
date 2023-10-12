from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from capturerrbackend.app.models.potion_ingredient import Ingredient, Potion
from capturerrbackend.app.schemas.potion_ingredient import (
    IngredientPayload,
    IngredientSchema,
    PotionPayload,
    PotionSchema,
)
from capturerrbackend.core.base.dependencies import get_repository
from capturerrbackend.core.base.repository import DatabaseRepository

router = APIRouter(prefix="/v2", tags=["v2"])

IngredientRepository = Annotated[
    DatabaseRepository[Ingredient],
    Depends(get_repository(Ingredient)),
]
PotionRepository = Annotated[
    DatabaseRepository[Potion],
    Depends(get_repository(Potion)),
]


@router.post("/ingredients", status_code=status.HTTP_201_CREATED)
async def create_ingredient(
    data: IngredientPayload,
    repository: IngredientRepository,
) -> IngredientSchema:
    ingredient = await repository.create(data.model_dump())
    return IngredientSchema.from_orm(ingredient)


@router.get("/ingredients", status_code=status.HTTP_200_OK)
async def get_ingredients(repository: IngredientRepository) -> list[IngredientSchema]:
    ingredients = await repository.filter()
    return [IngredientSchema.from_orm(ingredient) for ingredient in ingredients]


@router.get("/ingredients/{pk}", status_code=status.HTTP_200_OK)
async def get_ingredient(
    pk: int,
    repository: IngredientRepository,
) -> IngredientSchema:
    ingredient = await repository.get(pk)
    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient does not exist",
        )
    return IngredientSchema.model_validate(ingredient)


@router.post("/potions", status_code=status.HTTP_201_CREATED)
async def create_potion(
    data: PotionPayload,
    ingredient_repository: IngredientRepository,
    potion_repository: PotionRepository,
) -> PotionSchema:
    data_dict = data.model_dump()
    ingredients = await ingredient_repository.filter(
        Ingredient.pk.in_(data_dict.pop("ingredients")),
    )
    potion = await potion_repository.create({**data_dict, "ingredients": ingredients})
    return PotionSchema.model_validate(potion)


@router.get("/potions", status_code=status.HTTP_200_OK)
async def get_potions(repository: PotionRepository) -> list[PotionSchema]:
    potions = await repository.filter()
    return [PotionSchema.from_orm(potion) for potion in potions]


@router.get("/potions/{pk}", status_code=status.HTTP_200_OK)
async def get_potion(pk: int, repository: PotionRepository) -> PotionSchema:
    potion = await repository.get(pk)
    if potion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Potion does not exist",
        )

    return PotionSchema.from_orm(potion)

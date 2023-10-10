from pydantic import BaseModel, ConfigDict, Field


class IngredientSchema(BaseModel):
    """Ingredient model."""

    model_config = ConfigDict(from_attributes=True)

    pk: int
    name: str


class IngredientPayload(BaseModel):
    """Ingredient payload model."""

    name: str = Field(min_length=1, max_length=127)


class PotionSchema(BaseModel):
    """Potion model."""

    model_config = ConfigDict(from_attributes=True)

    pk: int
    name: str
    ingredients: list[IngredientSchema]


class PotionPayload(BaseModel):
    """Potion payload model."""

    name: str = Field(min_length=1, max_length=127)
    ingredients: list[int] = Field(min_items=1)

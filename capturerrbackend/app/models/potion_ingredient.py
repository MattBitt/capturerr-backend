from sqlalchemy import Column, ForeignKey, Integer, Table, orm

from capturerrbackend.core.base.model import Base

potion_ingredient_association = Table(
    "potion_ingredient",
    Base.metadata,
    Column("potion_pk", Integer, ForeignKey("potion.pk")),
    Column("ingredient_pk", Integer, ForeignKey("ingredient.pk")),
)


class Ingredient(Base):
    """Ingredient database model."""

    __tablename__ = "ingredient"

    name: orm.Mapped[str]


class Potion(Base):
    """Potion database model."""

    __tablename__ = "potion"

    name: orm.Mapped[str]
    ingredients: orm.Mapped[list["Ingredient"]] = orm.relationship(
        secondary=potion_ingredient_association,
        backref="potions",
        lazy="selectin",
    )

from abc import ABC, abstractmethod
from typing import override, Any

from sqlalchemy import select, Select

from .orm import meal_table
from .model import Meal
from ..sql import engine


class MealRepository(ABC):
    """
    Provides an interface to reconstitute existing meal from the persistent
    layer.
    """

    @classmethod
    @abstractmethod
    def get_from_id(self, id_: int) -> Meal | None:
        """
        Gets a meal from the persistent layer from the address id.
        """
        ...


class MealSqlRepository(MealRepository):

    @classmethod
    def _get_from_sqlalchemy_statement(
        cls, statement: Select[tuple[Any]]
    ) -> Meal | None:

        with engine.connect() as conn:
            meal_orm = conn.execute(statement).one_or_none()
            if meal_orm is None:
                return None
            meal = Meal(
                id=meal_orm.id,
                cuisine=meal_orm.cuisine,
                recipe=meal_orm.recipe,
                price=meal_orm.price,
            )

        return meal

    @override
    @classmethod
    def get_from_id(cls, id_: int) -> Meal | None:
        """
        Gets a meal from the persistent layer from the user's email.
        """

        statement = select(meal_table).where(meal_table.c.id == id_)

        return cls._get_from_sqlalchemy_statement(statement)


def get_meal_repository() -> MealRepository:
    return MealSqlRepository()

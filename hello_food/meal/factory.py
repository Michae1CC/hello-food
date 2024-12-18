from abc import ABC, abstractmethod
from typing import override, Any, Mapping

from sqlalchemy import insert

from .orm import meal_table
from .model import Meal
from ..mixins import JsonFactory
from ..sql import engine


class MealFactory(JsonFactory[Meal], ABC):

    @classmethod
    @abstractmethod
    def create_from_values(
        self,
        cuisine: str,
        recipe: str,
        price: float,
    ) -> Meal:
        """
        Create a new meal using the provided parameters.
        """
        ...


class MealSqlFactory(MealFactory):

    @override
    @classmethod
    def create_from_values(
        self,
        cuisine: str,
        recipe: str,
        price: float,
    ) -> Meal:

        with engine.connect() as connection:
            statement = (
                insert(meal_table)
                .values(
                    cuisine=cuisine,
                    recipe=recipe,
                    price=price,
                )
                .returning(meal_table.c.id)
            )
            meal_id = connection.execute(statement).scalar_one()
            connection.commit()

        return Meal(id=meal_id, cuisine=cuisine, recipe=recipe, price=price)

    @override
    @classmethod
    def create_from_json(cls, json_as_dict: Mapping[str, Any]) -> Meal:

        cuisine = cls._parse_str_from_json(json_as_dict, "cuisine")
        recipe = cls._parse_str_from_json(json_as_dict, "recipe")
        price = cls._parse_int_from_json(json_as_dict, "price")

        return cls.create_from_values(cuisine, recipe, price)


def get_meal_factory() -> MealFactory:
    return MealSqlFactory()

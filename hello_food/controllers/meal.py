from typing import Any, Mapping

from ..meal import Meal, get_meal_factory, get_meal_repository
from ..util import parse_str_from_json


def create_new_meal(meal_as_json_dict: Mapping[str, Any]) -> None:

    meal_factory = get_meal_factory()
    meal_factory.create_from_json(meal_as_json_dict)


def get_meals_from_cuisine(
    meals_from_cuisine_as_json_dict: Mapping[str, Any]
) -> list[Meal]:

    cuisine = parse_str_from_json(meals_from_cuisine_as_json_dict, "cuisine")

    meal_repository = get_meal_repository()
    return meal_repository.get_from_cuisine(cuisine)

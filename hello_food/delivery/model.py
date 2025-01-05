from typing import NamedTuple

from ..meal import Meal


class MealOrder(NamedTuple):
    meal_id: int
    quantity: int

    @classmethod
    def assert_quantity_is_positive_integer(cls, quantity: int) -> None:
        assert quantity > 0 and "Quantity must be greater than 0"


class Delivery:

    def __init__(
        self,
        id_: int,
        user_id: int,
        address_id: int,
        total: float,
        delivery_time: int,
        meal_orders: list[MealOrder],
    ) -> None:
        super().__init__()
        self.id: int = id_
        self.user_id: int = user_id
        self.address_id: int = address_id
        self.total: float = total
        self.delivery_time: int = delivery_time
        self.meal_orders: list[MealOrder] = meal_orders

    @classmethod
    def assert_delivery_date_is_unix_time_epoch(cls, delivery_time: int) -> None:
        assert delivery_time >= 0 and "Must be a valid Unix time epoch"

    @classmethod
    def compute_total(cls, meal_orders: list[MealOrder], meals: list[Meal]) -> float:

        total: float = 0.0
        meal_id_to_meal: dict[int, Meal] = {meal["id"]: meal for meal in meals}

        for meal_id, quantity in meal_orders:
            meal = meal_id_to_meal.get(meal_id)
            assert meal is not None and f"No meal found for meal_id {meal_id}"
            total += meal["price"] * quantity

        return total

    @classmethod
    def assert_total_is_sum_of_meal_orders(
        cls, total: float, meal_orders: list[MealOrder], meals: list[Meal]
    ) -> None:
        assert (
            total == cls.compute_total(meal_orders, meals)
            and "total does not match sum of meal orders"
        )

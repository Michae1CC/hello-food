from abc import ABC, abstractmethod
from typing import override, Any, Mapping

from sqlalchemy import insert

from .orm import delivery_table, meal_order_table
from .model import Delivery, MealOrder
from ..meal import get_meal_repository
from ..user import get_user_repository
from ..mixins import JsonFactory
from ..sql import engine


class DeliveryFactory(JsonFactory[Delivery], ABC):

    @classmethod
    @abstractmethod
    def create_from_values(
        self,
        user_id: int,
        address_id: int,
        meal_orders: list[tuple[int, int]],
    ) -> Delivery: ...


class DeliverySqlFactory(DeliveryFactory):

    @override
    @classmethod
    def create_from_values(
        self,
        user_id: int,
        address_id: int,
        meal_order_tuples: list[tuple[int, int]],
    ) -> Delivery:

        user_repository = get_user_repository()
        delivery_user = user_repository.get_from_id(user_id)
        assert delivery_user is not None and "Invalid user id given for delivery"

        assert (
            delivery_user.meals_per_week
            == sum(meal_tuple[1] for meal_tuple in meal_order_tuples)
            and "Number of meals in delivery does not match user meal constraint"
        )

        meal_orders: list[MealOrder] = [
            MealOrder(meal_id, quantity) for (meal_id, quantity) in meal_order_tuples
        ]

        for _, quantity in meal_order_tuples:
            MealOrder.assert_quantity_is_positive_integer(quantity)

        meal_ids = [meal_id for (meal_id, _) in meal_order_tuples]
        meal_repository = get_meal_repository()
        meals = meal_repository.get_from_ids(meal_ids)

        delivery_total = Delivery.compute_total(meal_orders, meals)

        with engine.connect() as connection:
            delivery_statement = (
                insert(delivery_table)
                .values(
                    user_id=user_id,
                    address_id=address_id,
                    total=delivery_total,
                )
                .returning(delivery_table.c.id)
            )
            delivery_id = connection.execute(delivery_statement).scalar_one()
            connection.commit()

            for meal_id, quantity in meal_order_tuples:
                meal_order_statement = insert(meal_order_table).values(
                    delivery_id=delivery_id, meal_id=meal_id, quantity=quantity
                )
                connection.execute(meal_order_statement)
            connection.commit()

        return Delivery(delivery_id, user_id, address_id, delivery_total, meal_orders)

    @override
    @classmethod
    def create_from_json(cls, json_as_dict: Mapping[str, Any]) -> Delivery:

        meal_orders_as_json: Any = json_as_dict.get("meal_orders")
        assert meal_orders_as_json is not None
        assert isinstance(meal_orders_as_json, list)

        meal_order_tuples: list[tuple[int, int]] = []
        for item in meal_orders_as_json:
            assert isinstance(item, dict)
            meal_id = cls._parse_int_from_json(item, "meal_id")
            quantity = cls._parse_int_from_json(item, "quantity")
            meal_order_tuples.append((meal_id, quantity))

        user_id = cls._parse_int_from_json(json_as_dict, "user_id")
        address_id = cls._parse_int_from_json(json_as_dict, "address_id")

        return cls.create_from_values(user_id, address_id, meal_order_tuples)


def get_delivery_factory() -> DeliveryFactory:
    return DeliverySqlFactory()

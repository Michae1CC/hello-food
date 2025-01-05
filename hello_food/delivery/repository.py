from abc import ABC, abstractmethod
from typing import override

from sqlalchemy import select

from .orm import delivery_table, meal_order_table
from .model import Delivery, MealOrder
from ..sql import engine


class DeliveryRepository(ABC):

    @classmethod
    @abstractmethod
    def get_from_id(self, id_: int) -> Delivery | None: ...


class DeliverySqlRepository(DeliveryRepository):

    @classmethod
    @override
    def get_from_id(self, id_: int) -> Delivery | None:

        with engine.connect() as connection:
            delivery_statement = select(delivery_table).where(
                delivery_table.c.id == id_
            )
            delivery_orm = connection.execute(delivery_statement).one_or_none()
            if delivery_orm is None:
                return None

            meal_orders_statement = select(meal_order_table).where(
                meal_order_table.c.delivery_id == id_
            )
            meal_orders_orm = connection.execute(meal_orders_statement).all()

        meal_orders = [
            MealOrder(meal_order_orm.meal_id, meal_order_orm.quantity)
            for meal_order_orm in meal_orders_orm
        ]
        return Delivery(
            id_,
            delivery_orm.user_id,
            delivery_orm.address_id,
            delivery_orm.total,
            delivery_orm.delivery_time,
            meal_orders,
        )


def get_delivery_repository() -> DeliveryRepository:
    return DeliverySqlRepository()

from typing import Any, Mapping
from sqlalchemy import select, Engine

import pytest

from hello_food import (
    engine,
    metadata,
    get_address_factory,
    get_delivery_factory,
    get_meal_factory,
    get_standard_user_factory,
    delivery_table,
    meal_order_table,
)


class TestAddressFactory:
    __test__ = True

    @pytest.fixture(scope="class")
    def db_engine(self):
        return engine

    @pytest.fixture(scope="function", autouse=True)
    def db_connection(self, db_engine):
        metadata.drop_all(db_engine)
        metadata.create_all(db_engine)
        yield
        metadata.drop_all(db_engine)

    def test_create_from_values_passes(self, db_engine: Engine) -> None:
        address_factory = get_address_factory()
        delivery_factory = get_delivery_factory()
        meal_factory = get_meal_factory()
        standard_user_factory = get_standard_user_factory()

        # Create an address
        assigned_unit = "Unit 18"
        assigned_street_name = "Wattle"
        assigned_suburb = "Cannon Hill"
        assigned_postcode = 4170

        created_address = address_factory.create_from_values(
            assigned_unit, assigned_street_name, assigned_suburb, assigned_postcode
        )

        # Create a trial user
        assigned_email = "test@example.com"
        assigned_name = "John Doe"
        assigned_meals_per_week = 1

        created_standard_user = standard_user_factory.create_from_values(
            assigned_email,
            assigned_name,
            assigned_meals_per_week,
            created_address.id,
        )

        # Create two meals
        assigned_meal_1_cuisine = "Italian"
        assigned_meal_1_recipe = "A lot of flour"
        assigned_meal_1_price = 8.90

        created_meal_1 = meal_factory.create_from_values(
            assigned_meal_1_cuisine, assigned_meal_1_recipe, assigned_meal_1_price
        )

        assigned_meal_2_cuisine = "Chinese"
        assigned_meal_2_recipe = "Pork"
        assigned_meal_2_price = 10.90

        created_meal_2 = meal_factory.create_from_values(
            assigned_meal_2_cuisine, assigned_meal_2_recipe, assigned_meal_2_price
        )

        # Create a delivery
        assigned_delivery_time = 123456
        assigned_meal_order_tuples = [
            (created_meal_1["id"], 1),
            (created_meal_2["id"], 3),
        ]

        created_delivery = delivery_factory.create_from_values(
            created_standard_user.id,
            created_address.id,
            assigned_delivery_time,
            assigned_meal_order_tuples,
        )

        assert created_delivery.user_id == created_standard_user.id
        assert created_delivery.address_id == created_address.id
        assert created_delivery.delivery_time == assigned_delivery_time

        delivery_statement = select(delivery_table).where(
            delivery_table.c.id == created_delivery.id
        )
        meal_orders_statement = select(meal_order_table).where(
            meal_order_table.c.delivery_id == created_delivery.id
        )

        with db_engine.connect() as connection:
            delivery_orm = connection.execute(delivery_statement).one()
            meal_orders_orm = connection.execute(meal_orders_statement).all()

        assert delivery_orm.user_id == created_standard_user.id
        assert delivery_orm.address_id == created_address.id
        assert delivery_orm.delivery_time == assigned_delivery_time
        assert set(
            (meal_order_orm.meal_id, meal_order_orm.quantity)
            for meal_order_orm in meal_orders_orm
        ) == set(assigned_meal_order_tuples)

    def test_create_from_json_passes(self, db_engine: Engine) -> None:
        address_factory = get_address_factory()
        delivery_factory = get_delivery_factory()
        meal_factory = get_meal_factory()
        standard_user_factory = get_standard_user_factory()

        # Create an address
        assigned_unit = "Unit 18"
        assigned_street_name = "Wattle"
        assigned_suburb = "Cannon Hill"
        assigned_postcode = 4170

        created_address = address_factory.create_from_values(
            assigned_unit, assigned_street_name, assigned_suburb, assigned_postcode
        )

        # Create a trial user
        assigned_email = "test@example.com"
        assigned_name = "John Doe"
        assigned_meals_per_week = 1

        created_standard_user = standard_user_factory.create_from_values(
            assigned_email,
            assigned_name,
            assigned_meals_per_week,
            created_address.id,
        )

        # Create two meals
        assigned_meal_1_cuisine = "Italian"
        assigned_meal_1_recipe = "A lot of flour"
        assigned_meal_1_price = 8.90

        created_meal_1 = meal_factory.create_from_values(
            assigned_meal_1_cuisine, assigned_meal_1_recipe, assigned_meal_1_price
        )

        assigned_meal_2_cuisine = "Chinese"
        assigned_meal_2_recipe = "Pork"
        assigned_meal_2_price = 10.90

        created_meal_2 = meal_factory.create_from_values(
            assigned_meal_2_cuisine, assigned_meal_2_recipe, assigned_meal_2_price
        )

        # Create a delivery
        assigned_delivery_time = 123456
        assigned_meal_order_1_quantity = 1
        assigned_meal_order_2_quantity = 3

        delivery_json: Mapping[str, Any] = {
            "user_id": created_standard_user.id,
            "address_id": created_address.id,
            "delivery_time": assigned_delivery_time,
            "meal_orders": [
                {
                    "meal_id": created_meal_1["id"],
                    "quantity": assigned_meal_order_1_quantity,
                },
                {
                    "meal_id": created_meal_2["id"],
                    "quantity": assigned_meal_order_2_quantity,
                },
            ],
        }

        created_delivery = delivery_factory.create_from_json(delivery_json)

        assert created_delivery.user_id == created_standard_user.id
        assert created_delivery.address_id == created_address.id
        assert created_delivery.delivery_time == assigned_delivery_time

        delivery_statement = select(delivery_table).where(
            delivery_table.c.id == created_delivery.id
        )
        meal_orders_statement = select(meal_order_table).where(
            meal_order_table.c.delivery_id == created_delivery.id
        )

        with db_engine.connect() as connection:
            delivery_orm = connection.execute(delivery_statement).one()
            meal_orders_orm = connection.execute(meal_orders_statement).all()

        assert delivery_orm.user_id == created_standard_user.id
        assert delivery_orm.address_id == created_address.id
        assert delivery_orm.delivery_time == assigned_delivery_time
        assert set(
            (meal_order_orm.meal_id, meal_order_orm.quantity)
            for meal_order_orm in meal_orders_orm
        ) == {
            (created_meal_1["id"], assigned_meal_order_1_quantity),
            (created_meal_2["id"], assigned_meal_order_2_quantity),
        }

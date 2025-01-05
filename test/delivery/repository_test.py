from typing import Generator

import pytest

from sqlalchemy import Engine, insert

from hello_food import (
    engine,
    metadata,
    MealOrder,
    Delivery,
    get_address_factory,
    get_delivery_repository,
    get_meal_factory,
    get_standard_user_factory,
    delivery_table,
    meal_order_table,
)


class TestAddressFactory:
    __test__ = True

    @pytest.fixture(scope="class")
    def db_engine(self) -> Engine:
        return engine

    @pytest.fixture(scope="function", autouse=True)
    def db_connection(self, db_engine: Engine) -> Generator[None, None, None]:
        metadata.drop_all(db_engine)
        metadata.create_all(db_engine)
        yield
        metadata.drop_all(db_engine)

    def test_get_from_id_passes_not_none(self, db_engine: Engine) -> None:
        address_factory = get_address_factory()
        meal_factory = get_meal_factory()
        standard_user_factory = get_standard_user_factory()
        delivery_repository = get_delivery_repository()

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
        assigned_meal_order_tuples = [
            (created_meal_1["id"], 1),
            (created_meal_2["id"], 3),
        ]
        meal_orders = [
            MealOrder(meal_id, quantity)
            for (meal_id, quantity) in assigned_meal_order_tuples
        ]

        delivery_total = Delivery.compute_total(
            meal_orders, [created_meal_1, created_meal_2]
        )

        with engine.connect() as connection:
            delivery_statement = (
                insert(delivery_table)
                .values(
                    user_id=created_standard_user.id,
                    address_id=created_address.id,
                    total=delivery_total,
                )
                .returning(delivery_table.c.id)
            )
            delivery_id = connection.execute(delivery_statement).scalar_one()
            connection.commit()

            for meal_id, quantity in assigned_meal_order_tuples:
                meal_order_statement = insert(meal_order_table).values(
                    delivery_id=delivery_id, meal_id=meal_id, quantity=quantity
                )
                connection.execute(meal_order_statement)
            connection.commit()

        retrieved_delivery = delivery_repository.get_from_id(delivery_id)

        assert retrieved_delivery is not None
        assert retrieved_delivery.user_id == created_standard_user.id
        assert retrieved_delivery.address_id == created_address.id
        assert set(retrieved_delivery.meal_orders) == set(meal_orders)

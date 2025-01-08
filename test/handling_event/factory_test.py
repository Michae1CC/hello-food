from sqlalchemy import select, Engine

import pytest

from hello_food import (
    engine,
    metadata,
    get_address_factory,
    get_handling_event_factory,
    get_delivery_factory,
    get_meal_factory,
    get_standard_user_factory,
    handling_event_table,
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
        handling_event_factory = get_handling_event_factory()
        meal_factory = get_meal_factory()
        standard_user_factory = get_standard_user_factory()

        # Create a from address
        assigned_from_unit = ""
        assigned_from_street_name = "Highland"
        assigned_from_suburb = "Fitzroy"
        assigned_from_postcode = 4300

        created_from_address = address_factory.create_from_values(
            assigned_from_unit,
            assigned_from_street_name,
            assigned_from_suburb,
            assigned_from_postcode,
        )

        # Create a to address
        assigned_to_unit = "Unit 18"
        assigned_to_street_name = "Wattle"
        assigned_to_suburb = "Cannon Hill"
        assigned_to_postcode = 4170

        created_to_address = address_factory.create_from_values(
            assigned_to_unit,
            assigned_to_street_name,
            assigned_to_suburb,
            assigned_to_postcode,
        )

        # Create a trial user
        assigned_email = "test@example.com"
        assigned_name = "John Doe"
        assigned_meals_per_week = 1

        created_standard_user = standard_user_factory.create_from_values(
            assigned_email,
            assigned_name,
            assigned_meals_per_week,
            created_to_address.id,
        )

        # Create two meals
        assigned_meal_1_cuisine = "Italian"
        assigned_meal_1_recipe = "A lot of flour"
        assigned_meal_1_price = 8.90

        created_meal_1 = meal_factory.create_from_values(
            assigned_meal_1_cuisine, assigned_meal_1_recipe, assigned_meal_1_price
        )

        # Create a delivery
        assigned_meal_order_tuples = [
            (created_meal_1["id"], 1),
        ]

        created_delivery = delivery_factory.create_from_values(
            created_standard_user.id,
            created_to_address.id,
            assigned_meal_order_tuples,
        )

        # Create handling event
        assigned_delivery_id = created_delivery.id
        assigned_to_address_id = created_to_address.id
        assigned_from_address_id = created_from_address.id
        assigned_completion_time = 123456

        created_handling_event = handling_event_factory.create_from_values(
            assigned_delivery_id,
            assigned_to_address_id,
            assigned_from_address_id,
            assigned_completion_time,
        )

        handling_event_statement = select(handling_event_table).where(
            handling_event_table.c.id == created_handling_event.id
        )

        with db_engine.connect() as connection:
            handling_event_orm = connection.execute(handling_event_statement).one()

        assert handling_event_orm.delivery_id == assigned_delivery_id
        assert handling_event_orm.to_address_id == assigned_to_address_id
        assert handling_event_orm.from_address_id == assigned_from_address_id
        assert handling_event_orm.completion_time == assigned_completion_time

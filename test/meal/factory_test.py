from typing import Generator

from sqlalchemy import select, Engine

import pytest

from hello_food import engine, metadata, meal_table, Meal, get_meal_factory


class TestTrialUserFactory:
    __test__ = True

    @pytest.fixture(scope="class")
    def db_engine(self):
        return engine

    @pytest.fixture(scope="function", autouse=True)
    def db_connection(self, db_engine: Engine) -> Generator[None, None, None]:
        metadata.drop_all(db_engine)
        metadata.create_all(db_engine)
        yield
        metadata.drop_all(db_engine)

    def test_create_from_values_passes(self, db_engine: Engine) -> None:
        meal_factory = get_meal_factory()

        assigned_cuisine = "Italian"
        assigned_recipe = "A lot of flour"
        assigned_price = 8.90

        created_meal = meal_factory.create_from_values(
            assigned_cuisine, assigned_recipe, assigned_price
        )

        assert created_meal["cuisine"] == assigned_cuisine
        assert created_meal["recipe"] == assigned_recipe
        assert created_meal["price"] == assigned_price

        meal_statement = select(meal_table).where(meal_table.c.id == meal_table.c.id)

        with db_engine.connect() as connection:
            meal_orm = connection.execute(meal_statement).one()

        assert meal_orm is not None
        assert meal_orm.id == created_meal["id"]
        assert meal_orm.cuisine == assigned_cuisine
        assert meal_orm.recipe == assigned_recipe
        assert meal_orm.price == assigned_price

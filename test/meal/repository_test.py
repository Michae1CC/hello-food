from typing import Generator

import pytest

from sqlalchemy import Engine, insert

from hello_food import engine, metadata, meal_table, Meal, get_meal_repository


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
        meal_repository = get_meal_repository()

        assigned_cuisine = "Italian"
        assigned_recipe = "A lot of flour"
        assigned_price = 8.90

        with db_engine.connect() as connection:
            statement = (
                insert(meal_table)
                .values(
                    cuisine=assigned_cuisine,
                    recipe=assigned_recipe,
                    price=assigned_price,
                )
                .returning(meal_table.c.id)
            )
            meal_id = connection.execute(statement).scalar_one()
            connection.commit()

        retrieved_meal = meal_repository.get_from_id(meal_id)

        assert retrieved_meal is not None
        assert retrieved_meal["id"] == meal_id
        assert retrieved_meal["cuisine"] == assigned_cuisine
        assert retrieved_meal["recipe"] == assigned_recipe
        assert retrieved_meal["price"] == assigned_price

from typing import Generator

from sqlalchemy import select, insert, Engine

import pytest

from hello_food import (
    engine,
    metadata,
    address_table,
    trial_user_table,
    user_table,
    get_trial_user_factory,
    get_standard_user_factory,
)


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
        trial_user_factory = get_trial_user_factory()

        with db_engine.connect() as connection:
            statement = (
                insert(address_table)
                .values(
                    unit="test_unit",
                    street_name="test_street",
                    suburb="test_suburb",
                    postcode=1,
                )
                .returning(address_table.c.id)
            )
            address_id = connection.execute(statement).scalar_one()
            connection.commit()

        assigned_email = "test@example.com"
        assigned_name = "John Doe"
        assigned_meals_per_week = 1
        assigned_discount_value = 0.2
        assigned_trial_end_date = 16_000

        created_trial_user = trial_user_factory.create_from_values(
            assigned_email,
            assigned_name,
            assigned_meals_per_week,
            assigned_trial_end_date,
            assigned_discount_value,
            address_id,
        )

        user_statement = select(user_table).where(
            user_table.c.id == created_trial_user.id
        )

        with db_engine.connect() as connection:
            user_orm = connection.execute(user_statement).one()

        assert user_orm is not None
        assert user_orm.email == assigned_email
        assert user_orm.name == assigned_name
        assert user_orm.meals_per_week == assigned_meals_per_week

        trial_user_statement = select(trial_user_table).where(
            trial_user_table.c.id == created_trial_user.id
        )

        with db_engine.connect() as connection:
            trial_user_orm = connection.execute(trial_user_statement).one()

        assert trial_user_orm.trial_end_date == assigned_trial_end_date
        assert trial_user_orm.discount_value == assigned_discount_value


class TestStandardUserFactory:
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
        standard_user_factory = get_standard_user_factory()

        with db_engine.connect() as connection:
            statement = (
                insert(address_table)
                .values(
                    unit="test_unit",
                    street_name="test_street",
                    suburb="test_suburb",
                    postcode=1,
                )
                .returning(address_table.c.id)
            )
            address_id = connection.execute(statement).scalar_one()
            connection.commit()

        assigned_email = "test@example.com"
        assigned_name = "John Doe"
        assigned_meals_per_week = 1

        created_standard_user = standard_user_factory.create_from_values(
            assigned_email,
            assigned_name,
            assigned_meals_per_week,
            address_id,
        )

        user_statement = select(user_table).where(
            user_table.c.id == created_standard_user.id
        )

        with db_engine.connect() as connection:
            user_orm = connection.execute(user_statement).one()

        assert user_orm is not None
        assert user_orm.email == assigned_email
        assert user_orm.name == assigned_name
        assert user_orm.meals_per_week == assigned_meals_per_week

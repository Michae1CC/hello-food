from typing import Generator

import pytest

from sqlalchemy import Engine, insert

from hello_food import (
    engine,
    metadata,
    address_table,
    user_table,
    standard_user_table,
    trial_user_table,
    get_user_repository,
    get_standard_user_repository,
    get_trial_user_repository,
)


class TestStandardUserRepository:
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

    def test_standard_user_get_from_email_passes_not_none(
        self, db_engine: Engine
    ) -> None:
        standard_user_repository = get_standard_user_repository()

        assigned_email = "test@example.com"
        assigned_name = "John Doe"
        assigned_meals_per_week = 1

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

            user_statement = (
                insert(user_table)
                .values(
                    email=assigned_email,
                    name=assigned_name,
                    meals_per_week=assigned_meals_per_week,
                    address_id=address_id,
                    type="standard_user",
                )
                .returning(user_table.c.id)
            )
            user_id = connection.execute(user_statement).scalar_one()
            standard_user_statement = insert(standard_user_table).values(
                id=user_id,
            )
            connection.execute(standard_user_statement)
            connection.commit()

        retrieved_standard_user = standard_user_repository.get_from_email(
            assigned_email
        )

        assert retrieved_standard_user is not None
        assert retrieved_standard_user.email == assigned_email
        assert retrieved_standard_user.name == assigned_name
        assert retrieved_standard_user.meals_per_week == assigned_meals_per_week
        assert retrieved_standard_user.address_id == address_id

    def test_standard_user_get_from_email_passes_none(self, db_engine: Engine) -> None:
        standard_user_repository = get_standard_user_repository()

        retrieved_standard_user = standard_user_repository.get_from_email(
            "test@example.com"
        )

        assert retrieved_standard_user is None


class TestTrialUserRepository:
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

    def test_trial_user_get_from_email_passes_not_none(self, db_engine: Engine) -> None:
        trial_user_repository = get_trial_user_repository()

        assigned_email = "test@example.com"
        assigned_name = "John Doe"
        assigned_meals_per_week = 1
        assigned_discount_value = 0.2
        assigned_trial_end_date = 16_000

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

            user_statement = (
                insert(user_table)
                .values(
                    email=assigned_email,
                    name=assigned_name,
                    meals_per_week=assigned_meals_per_week,
                    address_id=address_id,
                    type="trial_user",
                )
                .returning(user_table.c.id)
            )
            user_id = connection.execute(user_statement).scalar_one()
            trial_user_statement = insert(trial_user_table).values(
                id=user_id,
                trial_end_date=assigned_trial_end_date,
                discount_value=assigned_discount_value,
            )
            connection.execute(trial_user_statement)
            connection.commit()

        retrieved_trial_user = trial_user_repository.get_from_email(assigned_email)

        assert retrieved_trial_user is not None
        assert retrieved_trial_user.email == assigned_email
        assert retrieved_trial_user.name == assigned_name
        assert retrieved_trial_user.meals_per_week == assigned_meals_per_week
        assert retrieved_trial_user.address_id == address_id
        assert retrieved_trial_user.trial_end_date == assigned_trial_end_date
        assert retrieved_trial_user.discount_value == assigned_discount_value

    def test_trial_user_get_from_email_passes_none(self, db_engine: Engine) -> None:
        trial_user_repository = get_trial_user_repository()
        retrieved_trial_user = trial_user_repository.get_from_email("noexist@email.com")

        assert retrieved_trial_user is None


class TestUserRepository:
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

    def test_standard_user_get_from_email_passes_not_none(
        self, db_engine: Engine
    ) -> None:
        user_repository = get_user_repository()

        assigned_email = "test@example.com"
        assigned_name = "John Doe"
        assigned_meals_per_week = 1

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

            user_statement = (
                insert(user_table)
                .values(
                    email=assigned_email,
                    name=assigned_name,
                    meals_per_week=assigned_meals_per_week,
                    address_id=address_id,
                    type="standard_user",
                )
                .returning(user_table.c.id)
            )
            user_id = connection.execute(user_statement).scalar_one()
            standard_user_statement = insert(standard_user_table).values(
                id=user_id,
            )
            connection.execute(standard_user_statement)
            connection.commit()

        retrieved_user = user_repository.get_from_email(assigned_email)

        assert retrieved_user is not None
        assert retrieved_user.email == assigned_email
        assert retrieved_user.name == assigned_name
        assert retrieved_user.meals_per_week == assigned_meals_per_week
        assert retrieved_user.address_id == address_id

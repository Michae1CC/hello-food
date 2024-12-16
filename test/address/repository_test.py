from typing import Generator

import pytest

from sqlalchemy import Engine, insert

from hello_food import engine, metadata, get_address_repository, address_table


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
        address_repo = get_address_repository()

        assigned_unit = "Unit 18"
        assigned_street_name = "Wattle"
        assigned_suburb = "Cannon Hill"
        assigned_postcode = 4170

        with engine.connect() as connection:
            statement = (
                insert(address_table)
                .values(
                    unit=assigned_unit,
                    street_name=assigned_street_name,
                    suburb=assigned_suburb,
                    postcode=assigned_postcode,
                )
                .returning(address_table.c.id)
            )
            address_id = connection.execute(statement).scalar_one()
            connection.commit()

        retrieved_address = address_repo.get_from_id(address_id)

        assert retrieved_address is not None
        assert retrieved_address.unit == assigned_unit
        assert retrieved_address.street_name == assigned_street_name
        assert retrieved_address.suburb == assigned_suburb
        assert retrieved_address.postcode == assigned_postcode

    def test_get_from_id_passes_none(self, db_engine: Engine) -> None:
        address_repo = get_address_repository()

        retrieved_address = address_repo.get_from_id(1)

        assert retrieved_address is None

from sqlalchemy import select

import pytest

from hello_food import engine, metadata, get_address_factory, address_table


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

    def test_create_from_values_passes(self, db_engine):
        address_factory = get_address_factory()

        assigned_unit = "Unit 18"
        assigned_street_name = "Wattle"
        assigned_suburb = "Cannon Hill"
        assigned_postcode = 4170

        created_address = address_factory.create_from_values(
            assigned_unit, assigned_street_name, assigned_suburb, assigned_postcode
        )

        assert created_address.unit == assigned_unit
        assert created_address.street_name == assigned_street_name
        assert created_address.suburb == assigned_suburb
        assert created_address.postcode == assigned_postcode

        statement = select(address_table).where(
            address_table.c.id == created_address.id
        )

        with db_engine.connect() as connection:
            address_orm = connection.execute(statement).one()

        assert address_orm is not None
        assert address_orm.unit == assigned_unit
        assert address_orm.street_name == assigned_street_name
        assert address_orm.suburb == assigned_suburb
        assert address_orm.postcode == assigned_postcode

    def test_create_from_values_fails_on_invalid_postcode(self, db_engine):
        with pytest.raises(AssertionError):
            address_factory = get_address_factory()

            assigned_unit = "Unit 18"
            assigned_street_name = "Wattle"
            assigned_suburb = "Cannon Hill"
            assigned_invalid_postcode = -1

            address_factory.create_from_values(
                assigned_unit,
                assigned_street_name,
                assigned_suburb,
                assigned_invalid_postcode,
            )

    def test_create_from_json_passes(self, db_engine):
        address_factory = get_address_factory()

        assigned_unit = "Unit 18"
        assigned_street_name = "Wattle"
        assigned_suburb = "Cannon Hill"
        assigned_postcode = 4170

        created_address = address_factory.create_from_json(
            {
                "unit": assigned_unit,
                "street_name": assigned_street_name,
                "suburb": assigned_suburb,
                "postcode": assigned_postcode,
            }
        )

        assert created_address.unit == assigned_unit
        assert created_address.street_name == assigned_street_name
        assert created_address.suburb == assigned_suburb
        assert created_address.postcode == assigned_postcode

        statement = select(address_table).where(
            address_table.c.id == created_address.id
        )

        with db_engine.connect() as connection:
            address_orm = connection.execute(statement).one()

        assert address_orm is not None
        assert address_orm.unit == assigned_unit
        assert address_orm.street_name == assigned_street_name
        assert address_orm.suburb == assigned_suburb
        assert address_orm.postcode == assigned_postcode

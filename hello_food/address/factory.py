from abc import ABC, abstractmethod
from typing import override, Any, Mapping

from sqlalchemy import insert

from .orm import address_table
from .model import Address
from ..mixins import JsonFactory
from ..sql import engine


class AddressFactory(JsonFactory[Address], ABC):

    @classmethod
    @abstractmethod
    def create_from_values(
        self,
        unit: str,
        street_name: str,
        suburb: str,
        postcode: int,
    ) -> Address:
        """
        Create a new address using the provided parameters.
        """
        ...


class AddressSqlFactory(AddressFactory):

    @override
    @classmethod
    def create_from_values(
        self,
        unit: str,
        street_name: str,
        suburb: str,
        postcode: int,
    ) -> Address:
        """
        Create a new address using the provided parameters.
        """

        Address.assert_is_valid_postcode(postcode)

        with engine.connect() as connection:
            statement = (
                insert(address_table)
                .values(
                    unit=unit,
                    street_name=street_name,
                    suburb=suburb,
                    postcode=postcode,
                )
                .returning(address_table.c.id)
            )
            address_id = connection.execute(statement).scalar_one()
            connection.commit()

        return Address(address_id, unit, street_name, suburb, postcode)

    @override
    @classmethod
    def create_from_json(cls, json_as_dict: Mapping[str, Any]) -> Address:

        unit = cls._parse_str_from_json(json_as_dict, "unit")
        street_name = cls._parse_str_from_json(json_as_dict, "street_name")
        suburb = cls._parse_str_from_json(json_as_dict, "suburb")
        postcode = cls._parse_int_from_json(json_as_dict, "postcode")

        return cls.create_from_values(unit, street_name, suburb, postcode)


def get_address_factory() -> AddressFactory:
    return AddressSqlFactory()

from abc import ABC, abstractmethod
from typing import override, Any, Mapping

from sqlalchemy import select, Select

from .model import Address
from .orm import address_table
from ..sql import engine


class AddressRepository(ABC):
    """
    Provides an interface to reconstitute existing addresses from the persistent
    layer.
    """

    @classmethod
    @abstractmethod
    def get_from_id(self, id_: int) -> Address | None:
        """
        Gets a address from the persistent layer from the address id.
        """
        ...


class AddressSqlRepository(AddressRepository):

    @classmethod
    def _get_from_sqlalchemy_statement(
        cls, statement: Select[tuple[Any]]
    ) -> Address | None:

        with engine.connect() as conn:
            address_orm = conn.execute(statement).scalar_one_or_none()
            if address_orm is None:
                return None
            address = Address(
                address_orm.id,
                address_orm.unit,
                address_orm.street_name,
                address_orm.suburb,
                address_orm.postcode,
            )

        return address

    @override
    @classmethod
    def get_from_id(cls, id_: int) -> Address | None:
        """
        Gets a user from the persistent layer from the user's email.
        """

        statement = select(address_table).where(address_table.c.id == id_)

        return cls._get_from_sqlalchemy_statement(statement)


def get_address_repository() -> AddressRepository:
    return AddressSqlRepository()

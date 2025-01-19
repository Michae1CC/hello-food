from abc import ABC, abstractmethod
from typing import override, Any, Mapping

from sqlalchemy import insert

from .model import User, TrialUser, StandardUser
from ..address import Address, get_address_factory
from .orm import user_table, trial_user_table, standard_user_table
from ..log import Identified
from ..sql import engine
from ..mixins import JsonFactory


class TrialUserFactory(JsonFactory[TrialUser], ABC):
    """
    Provides an interface to create new users and commit them to the persistent
    layer.
    """

    @classmethod
    @abstractmethod
    def create_from_values(
        self,
        email: str,
        name: str,
        meals_per_week: int,
        trial_end_date: int,
        discount_value: float,
        address_id: int,
    ) -> TrialUser:
        """
        Create a new trial user using the provided parameters.
        """
        ...


class TrialUserSqlFactory(TrialUserFactory, Identified):
    """
    Provides an interface to create new users and commit them to the persistent
    layer.
    """

    @override
    @classmethod
    def create_from_values(
        cls,
        email: str,
        name: str,
        meals_per_week: int,
        trial_end_date: int,
        discount_value: float,
        address_id: int,
    ) -> TrialUser:
        """
        Each creation method is atomic and enforces all invariants of the
        created object or AGGREGATE. It should only be able to produce an
        object in a consistent state. For an ENTITY this means the creation of
        the entire AGGREGATE, with all invariants satisfied, but probably with
        optional elements still to be added. For an immutable VALUE this means
        all attributes are initialized to their correct final state. If
        the interface makes it possible to request an object that can't be
        created correctly, then an exception should be raised or some other
        mechanism should be invoked that will ensure that no improper return
        value is possible. pg 100
        """

        """
        A factory is responsible for ensuring all invariants are met for the
        object or AGGREGATE it creates; yet you should always think twice
        before removing the rules applying to an object outside that object.
        The factory can delegate invariant checking to the product, and this
        is often best. pg 103
        """

        User.assert_valid_base_user_values(email, name, meals_per_week)
        TrialUser.assert_trial_end_date_is_unix_time_epoch(trial_end_date)
        TrialUser.assert_discount_is_decimal_value(discount_value)

        with engine.connect() as connection:
            user_statement = (
                insert(user_table)
                .values(
                    email=email,
                    name=name,
                    meals_per_week=meals_per_week,
                    address_id=address_id,
                    type="trial_user",
                )
                .returning(user_table.c.id)
            )
            user_id = connection.execute(user_statement).scalar_one()
            trial_user_statement = insert(trial_user_table).values(
                id=user_id,
                trial_end_date=trial_end_date,
                discount_value=discount_value,
            )
            connection.execute(trial_user_statement)
            connection.commit()

            trial_user = TrialUser(
                user_id,
                email,
                name,
                meals_per_week,
                trial_end_date,
                discount_value,
                address_id,
            )

        return trial_user

    @override
    @classmethod
    def create_from_json(cls, json_as_dict: Mapping[str, Any]) -> TrialUser:
        """
        Creates a new user from a json representation of the user.
        """

        address_id = cls._parse_int_from_json(json_as_dict, "address_id")
        email = cls._parse_str_from_json(json_as_dict, "email")
        name = cls._parse_str_from_json(json_as_dict, "name")
        meals_per_week = cls._parse_int_from_json(json_as_dict, "meals_per_week")
        trial_end_date = cls._parse_int_from_json(json_as_dict, "trial_end_date")
        discount_value = cls._parse_float_from_json(json_as_dict, "discount_value")

        return cls.create_from_values(
            email, name, meals_per_week, trial_end_date, discount_value, address_id
        )


class StandardUserFactory(JsonFactory[StandardUser], ABC):
    """
    Provides an interface to create new users and commit them to the persistent
    layer.
    """

    @classmethod
    @abstractmethod
    def create_from_values(
        self,
        email: str,
        name: str,
        meals_per_week: int,
        address_id: int,
    ) -> StandardUser:
        """
        Create a new standard user using the provided parameters.
        """
        ...


class StandardUserSqlFactory(StandardUserFactory, Identified):
    """
    Provides an interface to create new users and commit them to the persistent
    layer.
    """

    @override
    @classmethod
    def create_from_values(
        cls,
        email: str,
        name: str,
        meals_per_week: int,
        address_id: int,
    ) -> StandardUser:

        User.assert_valid_base_user_values(email, name, meals_per_week)

        with engine.connect() as connection:
            user_statement = (
                insert(user_table)
                .values(
                    email=email,
                    name=name,
                    meals_per_week=meals_per_week,
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

            standard_user = StandardUser(
                user_id,
                email,
                name,
                meals_per_week,
                address_id,
            )

        return standard_user

    @override
    @classmethod
    def create_from_json(cls, json_as_dict: Mapping[str, Any]) -> StandardUser:
        """
        Creates a new standard user from a json representation of the user.
        """

        address_id = cls._parse_int_from_json(json_as_dict, "address_id")
        email = cls._parse_str_from_json(json_as_dict, "email")
        name = cls._parse_str_from_json(json_as_dict, "name")
        meals_per_week = cls._parse_int_from_json(json_as_dict, "meals_per_week")

        return cls.create_from_values(email, name, meals_per_week, address_id)


def get_trial_user_factory() -> TrialUserFactory:
    return TrialUserSqlFactory()


def get_standard_user_factory() -> StandardUserSqlFactory:
    return StandardUserSqlFactory()

from abc import ABC, abstractmethod
from typing import override, Any, Mapping

from .model import User, TrialUser, StandardUser
from ..address import Address, get_address_factory
from .orm import TrialUserORM, StandardUserORM
from ..log import Identified
from ..sql import session_maker
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

        User._assert_valid_base_user_values(email, name, meals_per_week)
        TrialUser._assert_trial_end_date_is_unix_time_epoch(trial_end_date)
        TrialUser._assert_discount_is_decimal_value(discount_value)

        with session_maker() as session:
            user_orm: TrialUserORM = TrialUserORM(
                name=name,
                email=email,
                meals_per_week=meals_per_week,
                trial_end_date=trial_end_date,
                discount_value=discount_value,
                address_id=address_id,
            )
            session.add(user_orm)
            session.commit()
            trial_user = TrialUser(
                user_orm.id,
                user_orm.email,
                user_orm.name,
                user_orm.meals_per_week,
                user_orm.trial_end_date,
                user_orm.discount_value,
                address_id,
            )

        return trial_user

    @override
    @classmethod
    def create_from_json(cls, json_as_dict: Mapping[str, Any]) -> TrialUser:
        """
        Creates a new user from a json representation of the user.
        """

        email = cls._parse_str_from_json(json_as_dict, "email")
        name = cls._parse_str_from_json(json_as_dict, "name")
        meals_per_week = cls._parse_int_from_json(json_as_dict, "meals_per_week")
        trial_end_date = cls._parse_int_from_json(json_as_dict, "trial_end_date")
        discount_value = cls._parse_float_from_json(json_as_dict, "discount_value")

        assert (
            isinstance(json_as_dict.get("address"), Mapping)
            and "Bad address information provided"
        )
        address_factory = get_address_factory()
        address: Address = address_factory.create_from_json(json_as_dict["address"])

        return cls.create_from_values(
            email, name, meals_per_week, trial_end_date, discount_value, address.id
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

        User._assert_valid_base_user_values(email, name, meals_per_week)

        with session_maker() as session:
            user_orm: StandardUserORM = StandardUserORM(
                name=name,
                email=email,
                meals_per_week=meals_per_week,
                address_id=address_id,
            )
            session.add(user_orm)
            session.commit()
            standard_user = StandardUser(
                user_orm.id,
                user_orm.email,
                user_orm.name,
                user_orm.meals_per_week,
                address_id,
            )

        return standard_user

    @override
    @classmethod
    def create_from_json(cls, json_as_dict: Mapping[str, Any]) -> StandardUser:
        """
        Creates a new standard user from a json representation of the user.
        """

        email = cls._parse_str_from_json(json_as_dict, "email")
        name = cls._parse_str_from_json(json_as_dict, "name")
        meals_per_week = cls._parse_int_from_json(json_as_dict, "meals_per_week")

        assert (
            isinstance(json_as_dict.get("address"), Mapping)
            and "Bad address information provided"
        )
        address_factory = get_address_factory()
        address: Address = address_factory.create_from_json(json_as_dict["address"])

        return cls.create_from_values(email, name, meals_per_week, address.id)


def get_trial_user_factory() -> TrialUserFactory:
    return TrialUserSqlFactory()


def get_standard_user_factory() -> StandardUserSqlFactory:
    return StandardUserSqlFactory()

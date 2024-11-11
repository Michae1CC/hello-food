import logging
from abc import ABC
from typing import Any, Self

from sqlalchemy import select, Select

from .orm import UserORM, TrialUserORM, PaidUserORM
from ..log import logger_level_property, Identified, class_logger
from ..mixins import JsonFactory
from ..sqlalchemy import Session


class User(Identified, ABC):

    level = logger_level_property()

    def __init__(self) -> None:
        self.level = logging.INFO

    @classmethod
    def _assert_email_has_valid_format(cls, email: str) -> None:
        import re

        valid = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        assert valid and f"Provided email of {email} is not valid"

    @classmethod
    def _assert_meals_per_week_is_positive_integer(cls, meals_per_week: int) -> None:
        assert meals_per_week > 0 and "Meals per week must be greater than 0"

    @classmethod
    def _assert_valid_base_user_values(
        cls, email: str, name: str, meals_per_week: int
    ) -> None:
        cls._assert_email_has_valid_format(email)
        cls._assert_meals_per_week_is_positive_integer(meals_per_week)


class TrialUser(User):

    def __init__(self, orm: TrialUserORM) -> None:
        super().__init__()
        self._orm = orm

    @classmethod
    def _assert_trial_end_date_is_unix_time_epoch(cls, trial_end_date: int) -> None:
        assert trial_end_date > 0 and "Must be a valid Unix time epoch"

    @classmethod
    def _assert_discount_is_decimal_value(cls, discount: float) -> None:
        assert (
            1 > discount > 0
            and "The discount value must be a decimal value between 0 and 1"
        )


class TrialUserRepository:
    """
    Provides an interface to reconstitute existing users from the persistent
    layer.
    """

    @classmethod
    def _get_from_sqlalchemy_statement(
        cls, statement: Select[tuple[TrialUserORM]]
    ) -> TrialUser:
        """
        Gets a user from the persistent layer using the provided sqlalchemy
        select statement.
        """

        with Session() as session:
            user_orm: TrialUserORM = session.execute(statement).scalar_one()

        return TrialUser(user_orm)

    @classmethod
    def get_from_id(cls, id: int) -> TrialUser:
        """
        Gets a user from the persistent layer from the user's id.
        """

        statement = select(TrialUserORM).where(TrialUserORM.id == id)

        return cls._get_from_sqlalchemy_statement(statement)

    @classmethod
    def get_from_email(cls, email: str) -> TrialUser:
        """
        Gets a user from the persistent layer from the user's email.
        """

        statement = select(TrialUserORM).where(TrialUserORM.email == email)

        return cls._get_from_sqlalchemy_statement(statement)


class TrialUserFactory(JsonFactory):
    """
    Provides an interface to create new users and commit them to the persistent
    layer.
    """

    @classmethod
    def create_from_values(
        cls,
        email: str,
        name: str,
        meals_per_week: int,
        trial_end_date: int,
        discount_value: float,
    ) -> TrialUser:
        """
        Create a new user using the provided parameters.
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

        user_orm: TrialUserORM = TrialUserORM(
            name=name,
            email=email,
            meals_per_week=meals_per_week,
            trial_end_date=trial_end_date,
            discount_value=discount_value,
        )

        with Session() as session:
            session.add(user_orm)
            session.commit()

        return TrialUser(user_orm)

    @classmethod
    def create_from_json(cls, json_as_dict: dict[str, Any]) -> TrialUser:
        """
        Creates a new user from a json representation of the user.
        """

        email = cls._parse_str_from_json(json_as_dict, "email")
        name = cls._parse_str_from_json(json_as_dict, "name")
        meals_per_week = cls._parse_int_from_json(json_as_dict, "meals_per_week")
        trial_end_date = cls._parse_int_from_json(json_as_dict, "trial_end_date")
        discount_value = cls._parse_float_from_json(json_as_dict, "discount_value")

        return cls.create_from_values(
            email, name, meals_per_week, trial_end_date, discount_value
        )

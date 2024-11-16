from abc import ABC, abstractmethod
from typing import override, Any, Mapping, Self

from sqlalchemy import select, Select

from .orm import UserORM, TrialUserORM, StandardUserORM
from ..util import get_current_unix_epoch
from ..log import logger_level_property, Identified, class_logger
from ..mixins import JsonFactory
from ..sql import session_maker


class User(ABC):

    def __init__(self, email: str, name: str, meals_per_week: int) -> None:
        super().__init__()
        self.email: str = email
        self.name: str = name
        self.meals_per_week = meals_per_week

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

    @abstractmethod
    def get_user_discount_as_decimal(self) -> float: ...

    @abstractmethod
    def is_locked_from_due_payment(self) -> bool: ...


class TrialUser(User):

    def __init__(
        self,
        email: str,
        name: str,
        meals_per_week: int,
        trial_end_date: int,
        discount_value: float,
    ) -> None:
        super().__init__(email, name, meals_per_week)
        self.trial_end_date = trial_end_date
        self.discount_value = discount_value

    @classmethod
    def _assert_trial_end_date_is_unix_time_epoch(cls, trial_end_date: int) -> None:
        assert trial_end_date > 0 and "Must be a valid Unix time epoch"

    @classmethod
    def _assert_discount_is_decimal_value(cls, discount: float) -> None:
        assert (
            1 > discount > 0
            and "The discount value must be a decimal value between 0 and 1"
        )

    @classmethod
    def from_orm(cls, orm: TrialUserORM) -> Self:
        return cls(
            orm.email,
            orm.name,
            orm.meals_per_week,
            orm.trial_end_date,
            orm.discount_value,
        )

    def __str__(self) -> str:
        return f"TrialUser(name={self.name}, email={self.email}, meals_per_week={self.meals_per_week}, trial_end_date={self.trial_end_date}, discount_value={self.discount_value})"

    @override
    def get_user_discount_as_decimal(self) -> float:
        return self.discount_value

    @override
    def is_locked_from_due_payment(self) -> bool:
        return self.trial_end_date < get_current_unix_epoch()


class TrialUserRepository(ABC):

    @classmethod
    @abstractmethod
    def get_from_email(self, email: str) -> TrialUser | None:
        """
        Gets a user from the persistent layer from the user's email.
        """
        ...


class TrialUserSqlRepository(TrialUserRepository, Identified):
    """
    Provides an interface to reconstitute existing users from the persistent
    layer. See pg 88
    """

    @classmethod
    def _get_from_sqlalchemy_statement(
        cls, statement: Select[tuple[TrialUserORM]]
    ) -> TrialUser | None:
        """
        Gets a user from the persistent layer using the provided sqlalchemy
        select statement.
        """

        with session_maker() as session:
            user_orm: TrialUserORM | None = session.execute(
                statement
            ).scalar_one_or_none()
            trial_user = TrialUser.from_orm(user_orm) if user_orm is not None else None

        return trial_user

    @override
    @classmethod
    def get_from_email(cls, email: str) -> TrialUser | None:
        """
        Gets a user from the persistent layer from the user's email.
        """

        statement = select(TrialUserORM).where(TrialUserORM.email == email)

        return cls._get_from_sqlalchemy_statement(statement)


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
    ) -> TrialUser:
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
            )
            session.add(user_orm)
            session.commit()
            trial_user = TrialUser.from_orm(user_orm)

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

        return cls.create_from_values(
            email, name, meals_per_week, trial_end_date, discount_value
        )


class StandardUser(User):

    def __init__(
        self,
        email: str,
        name: str,
        meals_per_week: int,
    ) -> None:
        super().__init__(email, name, meals_per_week)

    @classmethod
    def from_orm(cls, orm: StandardUserORM) -> Self:
        return cls(
            orm.email,
            orm.name,
            orm.meals_per_week,
        )

    def __str__(self) -> str:
        return f"StandardUser(name={self.name}, email={self.email}, meals_per_week={self.meals_per_week})"

    @override
    def get_user_discount_as_decimal(self) -> float:
        return 0.0

    @override
    def is_locked_from_due_payment(self) -> bool:
        return False


class StandardUserRepository(ABC):

    @classmethod
    @abstractmethod
    def get_from_email(self, email: str) -> StandardUser | None:
        """
        Gets a standard user from the persistent layer from the user's email.
        """
        ...


class StandardUserSqlRepository(StandardUserRepository, Identified):
    """
    Provides an interface to reconstitute existing standard users from the persistent
    layer. See pg 88
    """

    @classmethod
    def _get_from_sqlalchemy_statement(
        cls, statement: Select[tuple[StandardUserORM]]
    ) -> StandardUser | None:
        """
        Gets a standard user from the persistent layer using the provided sqlalchemy
        select statement.
        """

        with session_maker() as session:
            user_orm: StandardUserORM | None = session.execute(
                statement
            ).scalar_one_or_none()
            standard_user = (
                StandardUser.from_orm(user_orm) if user_orm is not None else None
            )

        return standard_user

    @override
    @classmethod
    def get_from_email(cls, email: str) -> StandardUser | None:
        """
        Gets a user from the persistent layer from the user's email.
        """

        statement = select(StandardUserORM).where(StandardUserORM.email == email)

        return cls._get_from_sqlalchemy_statement(statement)


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
    ) -> StandardUser:

        User._assert_valid_base_user_values(email, name, meals_per_week)

        with session_maker() as session:
            user_orm: StandardUserORM = StandardUserORM(
                name=name,
                email=email,
                meals_per_week=meals_per_week,
            )
            session.add(user_orm)
            session.commit()
            standard_user = StandardUser.from_orm(user_orm)

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

        return cls.create_from_values(email, name, meals_per_week)


class UserRepository(ABC):

    @classmethod
    @abstractmethod
    def get_from_email(self, email: str) -> User | None:
        """
        Gets an entity implementing the user interface from the persistent
        layer from the user's email.
        """
        ...


class UserSqlRepository(UserRepository, Identified):

    @override
    @classmethod
    def get_from_email(self, email: str) -> User | None:
        trial_user_repository = TrialUserSqlRepository()
        standard_user_repository = StandardUserSqlRepository()
        return trial_user_repository.get_from_email(
            email
        ) or standard_user_repository.get_from_email(email)

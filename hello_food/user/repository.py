from abc import ABC, abstractmethod
from typing import override

from sqlalchemy import select, Select

from .model import User, TrialUser, StandardUser
from .orm import TrialUserORM, StandardUserORM
from ..address import Address
from ..log import Identified
from ..sql import session_maker


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
            if user_orm is None:
                return None
            address_orm = user_orm.address
            address = Address(
                address_orm.id,
                address_orm.unit,
                address_orm.street_name,
                address_orm.suburb,
                address_orm.postcode,
            )
            trial_user = TrialUser(
                user_orm.email,
                user_orm.name,
                user_orm.meals_per_week,
                user_orm.trial_end_date,
                user_orm.discount_value,
                address,
            )

        return trial_user

    @override
    @classmethod
    def get_from_email(cls, email: str) -> TrialUser | None:
        """
        Gets a user from the persistent layer from the user's email.
        """

        statement = select(TrialUserORM).where(TrialUserORM.email == email)

        return cls._get_from_sqlalchemy_statement(statement)


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
            if user_orm is None:
                return None
            address_orm = user_orm.address
            address = Address(
                address_orm.id,
                address_orm.unit,
                address_orm.street_name,
                address_orm.suburb,
                address_orm.postcode,
            )
            standard_user = StandardUser(
                user_orm.email,
                user_orm.name,
                user_orm.meals_per_week,
                address,
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


def get_trial_user_repository() -> TrialUserRepository:
    return TrialUserSqlRepository()


def get_standard_user_repository() -> StandardUserRepository:
    return StandardUserSqlRepository()


def get_user_repository() -> UserRepository:
    return UserSqlRepository()

from abc import ABC, abstractmethod
from typing import override, Any

from sqlalchemy import select

from .model import User, TrialUser, StandardUser
from .orm import user_table, trial_user_table, standard_user_table
from ..log import Identified
from ..sql import engine


class TrialUserRepository(ABC):

    @classmethod
    @abstractmethod
    def get_from_id(self, id: int) -> TrialUser | None:
        """
        Gets a user from the persistent layer from the user's id.
        """
        ...

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
    @override
    def get_from_id(self, id: int) -> TrialUser | None:
        """
        Gets a user from the persistent layer from the user's id.
        """

        with engine.connect() as conn:
            user_table_statement = select(user_table).where(user_table.c.id == id)
            user_orm = conn.execute(user_table_statement).one_or_none()

            if user_orm is None:
                return None

            trial_user_table_statement = select(trial_user_table).where(
                trial_user_table.c.id == user_orm.id
            )
            trial_user_orm = conn.execute(trial_user_table_statement).one_or_none()

            if trial_user_orm is None:
                return None

            trial_user = TrialUser(
                user_orm.id,
                user_orm.email,
                user_orm.name,
                user_orm.meals_per_week,
                trial_user_orm.trial_end_date,
                trial_user_orm.discount_value,
                user_orm.address_id,
            )

        return trial_user

    @override
    @classmethod
    def get_from_email(cls, email: str) -> TrialUser | None:
        """
        Gets a user from the persistent layer from the user's email.
        """

        with engine.connect() as conn:
            user_table_statement = select(user_table).where(user_table.c.email == email)
            user_orm = conn.execute(user_table_statement).one_or_none()

            if user_orm is None:
                return None

            trial_user_table_statement = select(trial_user_table).where(
                trial_user_table.c.id == user_orm.id
            )
            trial_user_orm = conn.execute(trial_user_table_statement).one_or_none()

            if trial_user_orm is None:
                return None

            trial_user = TrialUser(
                user_orm.id,
                user_orm.email,
                user_orm.name,
                user_orm.meals_per_week,
                trial_user_orm.trial_end_date,
                trial_user_orm.discount_value,
                user_orm.address_id,
            )

        return trial_user


class StandardUserRepository(ABC):

    @classmethod
    @abstractmethod
    def get_from_id(self, id: int) -> StandardUser | None:
        """
        Gets a user from the persistent layer from the user's id.
        """
        ...

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
    @override
    def get_from_id(self, id: int) -> StandardUser | None:
        """
        Gets a user from the persistent layer from the user's id.
        """

        with engine.connect() as conn:
            user_table_statement = select(user_table).where(user_table.c.id == id)
            user_orm = conn.execute(user_table_statement).one_or_none()

            if user_orm is None:
                return None

            standard_user_table_statement = select(standard_user_table).where(
                standard_user_table.c.id == user_orm.id
            )
            standard_user_orm = conn.execute(
                standard_user_table_statement
            ).one_or_none()

            if standard_user_orm is None:
                return None

            standard_user = StandardUser(
                user_orm.id,
                user_orm.email,
                user_orm.name,
                user_orm.meals_per_week,
                user_orm.address_id,
            )

        return standard_user

    @override
    @classmethod
    def get_from_email(cls, email: str) -> StandardUser | None:
        """
        Gets a user from the persistent layer from the user's email.
        """

        with engine.connect() as conn:
            user_table_statement = select(user_table).where(user_table.c.email == email)
            user_orm = conn.execute(user_table_statement).one_or_none()

            if user_orm is None:
                return None

            standard_user_table_statement = select(standard_user_table).where(
                standard_user_table.c.id == user_orm.id
            )
            standard_user_orm = conn.execute(
                standard_user_table_statement
            ).one_or_none()

            if standard_user_orm is None:
                return None

            standard_user = StandardUser(
                user_orm.id,
                user_orm.email,
                user_orm.name,
                user_orm.meals_per_week,
                user_orm.address_id,
            )

        return standard_user


class UserRepository(ABC):

    @classmethod
    @abstractmethod
    def get_from_id(self, id: int) -> User | None:
        """
        Gets an entity implementing the user interface from the persistent
        layer from the user's id.
        """
        ...

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
    def get_from_id(self, id: int) -> User | None:
        trial_user_repository = TrialUserSqlRepository()
        standard_user_repository = StandardUserSqlRepository()
        return trial_user_repository.get_from_id(
            id
        ) or standard_user_repository.get_from_id(id)

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

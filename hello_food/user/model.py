from abc import ABC, abstractmethod
from typing import override

from ..util import get_current_unix_epoch


class User(ABC):

    def __init__(
        self, id_: int, email: str, name: str, meals_per_week: int, address_id: int
    ) -> None:
        super().__init__()
        self.id: int = id_
        self.email: str = email
        self.name: str = name
        self.meals_per_week: int = meals_per_week
        self.address_id: int = address_id

    @classmethod
    def assert_email_has_valid_format(cls, email: str) -> None:
        import re

        valid = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        assert valid and f"Provided email of {email} is not valid"

    @classmethod
    def assert_meals_per_week_is_positive_integer(cls, meals_per_week: int) -> None:
        assert meals_per_week > 0 and "Meals per week must be greater than 0"

    @classmethod
    def assert_valid_base_user_values(
        cls, email: str, name: str, meals_per_week: int
    ) -> None:
        cls.assert_email_has_valid_format(email)
        cls.assert_meals_per_week_is_positive_integer(meals_per_week)

    @abstractmethod
    def get_user_discount_as_decimal(self) -> float: ...

    @abstractmethod
    def is_locked_from_due_payment(self) -> bool: ...


class TrialUser(User):

    def __init__(
        self,
        id_: int,
        email: str,
        name: str,
        meals_per_week: int,
        trial_end_date: int,
        discount_value: float,
        address_id: int,
    ) -> None:
        super().__init__(id_, email, name, meals_per_week, address_id)
        self.trial_end_date = trial_end_date
        self.discount_value = discount_value

    @classmethod
    def assert_trial_end_date_is_unix_time_epoch(cls, trial_end_date: int) -> None:
        assert trial_end_date > 0 and "Must be a valid Unix time epoch"

    @classmethod
    def assert_discount_is_decimal_value(cls, discount: float) -> None:
        assert (
            1 > discount > 0
            and "The discount value must be a decimal value between 0 and 1"
        )

    def __str__(self) -> str:
        return f"TrialUser(name={self.name}, email={self.email}, meals_per_week={self.meals_per_week}, trial_end_date={self.trial_end_date}, discount_value={self.discount_value})"

    @override
    def get_user_discount_as_decimal(self) -> float:
        return self.discount_value

    @override
    def is_locked_from_due_payment(self) -> bool:
        return self.trial_end_date < get_current_unix_epoch()


class StandardUser(User):

    def __init__(
        self,
        id_: int,
        email: str,
        name: str,
        meals_per_week: int,
        address_id: int,
    ) -> None:
        super().__init__(id_, email, name, meals_per_week, address_id)

    def __str__(self) -> str:
        return f"StandardUser(name={self.name}, email={self.email}, meals_per_week={self.meals_per_week})"

    @override
    def get_user_discount_as_decimal(self) -> float:
        return 0.0

    @override
    def is_locked_from_due_payment(self) -> bool:
        return False

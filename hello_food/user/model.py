from abc import abstractmethod, ABC
from typing import Any, Self

from ..mixins import FromJsonMixin


class User(FromJsonMixin, ABC):

    def __init__(self, email: str, name: str, meals_per_week: int) -> None:
        self.email: str = email
        self.name: str = name
        self.meals_per_week: int = meals_per_week


class TrialUser(User):

    def __init__(
        self, email: str, name: str, meals_per_week: int, trial_end_date: int
    ) -> None:
        super().__init__(email, name, meals_per_week)
        self.trial_end_date: int = trial_end_date

    @classmethod
    def from_json(cls, json_as_dict: dict[str, Any]) -> Self:
        email = cls._parse_str_from_json(json_as_dict, "email")
        name = cls._parse_str_from_json(json_as_dict, "name")
        meals_per_week = cls._parse_int_from_json(json_as_dict, "meals_per_week")
        trial_end_date = cls._parse_int_from_json(json_as_dict, "trial_end_date")

        return cls(email, name, meals_per_week, trial_end_date)

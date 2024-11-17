from typing import NamedTuple

from .orm import AddressORM


class Address(NamedTuple):
    id: int
    unit: str
    street_name: str
    suburb: str
    postcode: int

    @classmethod
    def _assert_is_valid_postcode(cls, postcode: int) -> None:
        assert 0 < postcode < 10_000 and f"Invalid postcode of {postcode} provided"

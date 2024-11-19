from typing import NamedTuple

from .orm import AddressORM


class Address:

    def __init__(
        self, id: int, unit: str, street_name: str, suburb: str, postcode: int
    ) -> None:
        super().__init__()
        self.id: int = id
        self.unit: str = unit
        self.street_name: str = street_name
        self.suburb: str = suburb
        self.postcode: int = postcode

    @classmethod
    def _assert_is_valid_postcode(cls, postcode: int) -> None:
        assert 0 < postcode < 10_000 and f"Invalid postcode of {postcode} provided"

import pytest

from hello_food import Address


class TestAddress:
    __test__ = True

    @pytest.mark.parametrize("postcode", (1, 42, 142, 4170, 9999))
    def test_assert_is_valid_postcode_for_valid_postcodes(self, postcode: int) -> None:
        Address.assert_is_valid_postcode(postcode)

    @pytest.mark.parametrize("postcode", (-42, -1, 0, 10_000, 100_000))
    def test_assert_is_valid_postcode_for_invalid_postcodes(
        self, postcode: int
    ) -> None:
        with pytest.raises(AssertionError):
            Address.assert_is_valid_postcode(postcode)

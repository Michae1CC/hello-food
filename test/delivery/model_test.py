import pytest

from hello_food import Delivery, Meal, MealOrder


class TestDelivery:
    __test__ = True

    @pytest.mark.parametrize("quantity", (1, 42, 142, 4170, 9999))
    def test_assert_quantity_is_positive_integer_passes(self, quantity: int) -> None:
        MealOrder.assert_quantity_is_positive_integer(quantity)

    @pytest.mark.parametrize("quantity", (-42, -1, 0))
    def test_assert_quantity_is_positive_integer_throws_assertion_error(
        self, quantity: int
    ) -> None:
        with pytest.raises(AssertionError):
            MealOrder.assert_quantity_is_positive_integer(quantity)

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

    @pytest.mark.parametrize("unix_time_epoch", (0, 1, 160000))
    def test_assert_delivery_date_is_unix_time_epoch_passes(
        self, unix_time_epoch: int
    ) -> None:
        Delivery.assert_delivery_date_is_unix_time_epoch(unix_time_epoch)

    @pytest.mark.parametrize("unix_time_epoch", (-42, -1))
    def test_assert_delivery_date_is_unix_time_epoch_throws_assertion_error(
        self, unix_time_epoch: int
    ) -> None:
        with pytest.raises(AssertionError):
            Delivery.assert_delivery_date_is_unix_time_epoch(unix_time_epoch)

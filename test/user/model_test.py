import pytest

from hello_food import User, TrialUser


class TestUser:
    __test__ = True

    @pytest.mark.parametrize("email", ("h@example.com", "mike@example.com"))
    def test_assert_email_has_valid_format_passes(self, email: str) -> None:
        User.assert_email_has_valid_format(email)

    @pytest.mark.parametrize("email", ("@example.com", "mike@example.c"))
    def test_assert_email_has_valid_format_throws_assertion_error(
        self, email: str
    ) -> None:
        with pytest.raises(AssertionError):
            User.assert_email_has_valid_format(email)

    @pytest.mark.parametrize("meals_per_week", (1, 10_000))
    def test_assert_meals_per_week_is_positive_integer_passes(
        self, meals_per_week: int
    ) -> None:
        User.assert_meals_per_week_is_positive_integer(meals_per_week)

    @pytest.mark.parametrize("meals_per_week", (-20, -1, 0))
    def test_assert_meals_per_week_is_positive_integer_throws_assertion_error(
        self, meals_per_week: int
    ) -> None:
        with pytest.raises(AssertionError):
            User.assert_meals_per_week_is_positive_integer(meals_per_week)


class TestTrialUser:
    __test__ = True

    @pytest.mark.parametrize("trail_end_date", (0.000001, 0.5, 1.0))
    def assert_discount_is_decimal_value_passes(cls, discount: float) -> None:
        TrialUser.assert_discount_is_decimal_value(discount)

    @pytest.mark.parametrize("trail_end_date", (-1, -0.0001, 0, 1.01, 2.0))
    def assert_discount_is_decimal_value_throws_assertion_error(
        cls, discount: float
    ) -> None:
        with pytest.raises(AssertionError):
            TrialUser.assert_discount_is_decimal_value(discount)

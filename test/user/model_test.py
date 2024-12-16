import pytest
from mock import patch

from hello_food import User, TrialUser, StandardUser


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

    @pytest.fixture
    def default_user_discount_value(self) -> float:
        return 0.2

    @pytest.fixture
    def default_user_trial_end_date(self) -> int:
        return 123456

    @pytest.fixture
    def default_user(
        self, default_user_discount_value: float, default_user_trial_end_date: int
    ) -> TrialUser:
        return TrialUser(
            0,
            "markerplier@example.com",
            "mark",
            2,
            default_user_trial_end_date,
            default_user_discount_value,
            0,
        )

    @pytest.mark.parametrize("discount", (0.000001, 0.5, 0.99))
    def test_assert_discount_is_decimal_value_passes(cls, discount: float) -> None:
        TrialUser.assert_discount_is_decimal_value(discount)

    @pytest.mark.parametrize("discount", (-1, -0.0001, 0, 1.0, 1.01, 2.0))
    def test_assert_discount_is_decimal_value_throws_assertion_error(
        cls, discount: float
    ) -> None:
        with pytest.raises(AssertionError):
            TrialUser.assert_discount_is_decimal_value(discount)

    def test_get_user_discount_as_decimal(
        self, default_user_discount_value: float, default_user: TrialUser
    ) -> None:
        assert (
            default_user.get_user_discount_as_decimal() == default_user_discount_value
        )

    @pytest.mark.parametrize(
        ("current_time", "locked_out"),
        ((123455, False), (123456, True), (123457, True)),
    )
    def test_is_locked_from_due_payment(
        self, current_time: int, locked_out: bool, default_user: TrialUser
    ) -> None:
        with patch("time.time") as time_mock:
            time_mock.return_value = current_time
            assert default_user.is_locked_from_due_payment() is locked_out


class TestStandardUser:

    @pytest.fixture
    def default_user(
        self,
    ) -> StandardUser:
        return StandardUser(
            0,
            "markerplier@example.com",
            "mark",
            3,
            0,
        )

    def test_get_user_discount_as_decimal(self, default_user: StandardUser) -> None:
        assert default_user.get_user_discount_as_decimal() == 0.0

    def test_is_locked_from_due_payment(self, default_user: StandardUser) -> None:
        assert default_user.is_locked_from_due_payment() is False

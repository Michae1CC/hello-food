from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ..sqlalchemy import Base


class UserORM(Base):
    __tablename__ = "User"
    email: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    meals_per_week: Mapped[int]
    type: Mapped[str]

    __mapper_args__ = {
        "polymorphic_abstract": True,
        "polymorphic_identity": "user",
        "polymorphic_on": "type",
    }


class TrialUserORM(UserORM):
    __tablename__ = "TrialUser"
    email: Mapped[str] = mapped_column(ForeignKey("User.email"), primary_key=True)
    trial_end_date: Mapped[int]
    discount_value: Mapped[float]

    __mapper_args__ = {
        "polymorphic_identity": "trail_user",
    }


class PaidUserORM(UserORM):
    __tablename__ = "PaidUser"
    email: Mapped[str] = mapped_column(ForeignKey("User.email"), primary_key=True)
    account_renewal_date: Mapped[int]

    __mapper_args__ = {
        "polymorphic_identity": "paid_user",
    }

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from ..sql import Base
from ..address import AddressORM


class UserORM(Base):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    meals_per_week: Mapped[int]
    address_id: Mapped[int] = mapped_column(ForeignKey("Address.id"))
    address: Mapped[AddressORM] = relationship()
    type: Mapped[str]

    __mapper_args__ = {
        "polymorphic_abstract": True,
        "polymorphic_identity": "user",
        "polymorphic_on": "type",
    }


class TrialUserORM(UserORM):
    __tablename__ = "TrialUser"
    id: Mapped[int] = mapped_column(ForeignKey("User.id"), primary_key=True)
    trial_end_date: Mapped[int]
    discount_value: Mapped[float]

    __mapper_args__ = {
        "polymorphic_identity": "trail_user",
    }


class StandardUserORM(UserORM):
    __tablename__ = "PaidUser"
    id: Mapped[int] = mapped_column(ForeignKey("User.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "paid_user",
    }

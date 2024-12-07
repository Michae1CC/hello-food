from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey

from ..sql import metadata

user_table = Table(
    "User",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String, nullable=True, unique=True),
    Column("name", String, nullable=True),
    Column("meals_per_week", Integer, nullable=True),
    Column("address_id", String, ForeignKey("Address.id"), nullable=True),
    Column("type", String, nullable=True),
)

trial_user_table = Table(
    "TrialUser",
    metadata,
    Column("id", Integer, ForeignKey("Address.id"), nullable=True),
    Column("trial_end_date", Integer, nullable=True),
    Column("discount_value", Float, nullable=True),
)

standard_user_table = Table(
    "StandardUser",
    metadata,
    Column("id", Integer, ForeignKey("Address.id"), nullable=True),
)

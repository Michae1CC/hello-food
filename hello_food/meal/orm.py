from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey

from ..sql import metadata

meal_table = Table(
    "Meal",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("cuisine", String, nullable=True),
    Column("recipe", String, nullable=True),
    Column("price", Float, nullable=True),
)

from sqlalchemy import Table, Column, Integer, Float, ForeignKey

from ..sql import metadata

meal_order_table = Table(
    "MealOrder",
    metadata,
    Column(
        "meal_id",
        Integer,
        ForeignKey("Meal.id"),
        primary_key=True,
    ),
    Column(
        "delivery_id",
        Integer,
        ForeignKey("Delivery.id"),
        primary_key=True,
    ),
    Column("quantity", Integer, nullable=False),
)

delivery_table = Table(
    "Delivery",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("User.id"), nullable=False),
    Column("address_id", Integer, ForeignKey("Address.id"), nullable=False),
    Column("total", Float, nullable=False),
)

from sqlalchemy import Table, Column, Integer, String

from ..sql import metadata

address_table = Table(
    "Address",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("unit", String, nullable=True),
    Column("street_name", String, nullable=False),
    Column("suburb", String, nullable=False),
    Column("postcode", Integer, nullable=False),
)

from sqlalchemy import Table, Column, Integer, ForeignKey

from ..sql import metadata

handling_event_table = Table(
    "HandlingTable",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("delivery_id", Integer, ForeignKey("Delivery.id")),
    Column("to_address_id", Integer, ForeignKey("Address.id")),
    Column("from_address_id", Integer, ForeignKey("Address.id")),
    Column("completion_time", Integer, nullable=False),
)

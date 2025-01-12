from functools import singledispatch
from typing import Any

from sqlalchemy import Connection, delete, update, select

from .sql import engine
from .address import Address, address_table
from .delivery import Delivery, delivery_table
from .user import (
    user_table,
    trial_user_table,
    User,
    TrialUser,
    StandardUser,
)

_PERSISTENT_ENTITIES = User | TrialUser | StandardUser | Address | Delivery


def update_sql_entities(*entities: _PERSISTENT_ENTITIES) -> None:

    with engine.connect() as connection:
        for entity in entities:
            _prepare_entity_for_update(entity, connection)


@singledispatch
def _prepare_entity_for_update(entity: Any, connection: Connection) -> None:
    raise ValueError(f"No update register for {type(entity).__name__}")


@_prepare_entity_for_update.register
def _(entity: Address, connection: Connection) -> None:

    update_base_statement = (
        update(address_table)
        .where(address_table.c.id == entity.id)
        .values(
            unit=entity.unit,
            street_name=entity.street_name,
            suburb=entity.suburb,
            postcode=entity.postcode,
        )
    )
    connection.execute(update_base_statement)


@_prepare_entity_for_update.register
def _(entity: Delivery, connection: Connection) -> None:

    update_statement = (
        update(delivery_table)
        .where(delivery_table.c.id == entity.id)
        .values(
            user_id=entity.user_id,
            address_id=entity.address_id,
            total=entity.total,
        )
    )
    connection.execute(update_statement)


@_prepare_entity_for_update.register
def _(entity: TrialUser, connection: Connection) -> None:

    update_base_statement = (
        update(user_table)
        .where(user_table.c.id == entity.id)
        .values(
            email=entity.email,
            name=entity.name,
            meals_per_week=entity.meals_per_week,
            address_id=entity.address_id,
        )
    )
    connection.execute(update_base_statement)

    update_child_statement = (
        update(trial_user_table)
        .where(trial_user_table.c.id == entity.id)
        .values(
            trial_end_date=entity.trial_end_date,
            discount_value=entity.discount_value,
        )
    )
    connection.execute(update_child_statement)


@_prepare_entity_for_update.register
def _(entity: StandardUser, connection: Connection) -> None:

    update_base_statement = (
        update(user_table)
        .where(user_table.c.id == entity.id)
        .values(
            email=entity.email,
            name=entity.name,
            meals_per_week=entity.meals_per_week,
            address_id=entity.address_id,
        )
    )
    connection.execute(update_base_statement)

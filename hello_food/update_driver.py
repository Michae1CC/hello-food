from functools import singledispatch
from typing import Any

from sqlalchemy import delete, update, select
from sqlalchemy.orm import Session

from .sql import session_maker
from .address import Address, AddressORM
from .user import User, UserORM, TrialUser, TrialUserORM, StandardUser

_PERSISTENT_ENTITIES = User | TrialUser | StandardUser | Address


def update_sql_entities(*entities: _PERSISTENT_ENTITIES) -> None:

    with session_maker() as session:
        for entity in entities:
            _prepare_entity_for_update(entity, session)
        session.commit()


@singledispatch
def _prepare_entity_for_update(entity: Any, session: Session) -> None:
    raise ValueError(f"No update register for {type(entity).__name__}")


@_prepare_entity_for_update.register
def _(entity: AddressORM, session: Session) -> None:

    update_base_statement = (
        update(AddressORM)
        .where(AddressORM.id == entity.id)
        .values(
            unit=entity.unit,
            street_name=entity.street_name,
            suburb=entity.suburb,
            postcode=entity.postcode,
        )
    )
    session.execute(update_base_statement)


@_prepare_entity_for_update.register
def _(entity: TrialUser, session: Session) -> None:

    # A single joined table update is not supported
    # https://github.com/sqlalchemy/sqlalchemy/discussions/10128

    update_base_statement = (
        update(UserORM)
        .where(UserORM.id == entity.id)
        .values(
            email=entity.email,
            name=entity.name,
            meals_per_week=entity.meals_per_week,
            address_id=entity.address_id,
        )
    )
    session.execute(update_base_statement)

    update_child_statement = (
        update(TrialUserORM)
        .where(TrialUserORM.id == entity.id)
        .values(
            trial_end_date=entity.trial_end_date,
            discount_value=entity.discount_value,
        )
    )
    session.execute(update_child_statement)


@_prepare_entity_for_update.register
def _(entity: StandardUser, session: Session) -> None:

    update_base_statement = (
        update(UserORM)
        .where(UserORM.id == entity.id)
        .values(
            email=entity.email,
            name=entity.name,
            meals_per_week=entity.meals_per_week,
            address_id=entity.address_id,
        )
    )
    session.execute(update_base_statement)

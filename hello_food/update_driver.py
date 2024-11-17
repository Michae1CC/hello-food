from functools import singledispatch
from typing import Any

from sqlalchemy import delete, update, select
from sqlalchemy.orm import Session

from .sql import session_maker
from .address import Address, AddressORM
from .user import User, UserORM, TrialUser, TrialUserORM, StandardUser

_PERSISTENT_ENTITIES = User | TrialUser | StandardUser


def update_user_address(entity: User, session: Session) -> None:

    user_orm: UserORM = session.execute(
        select(UserORM).where(UserORM.email == entity.email)
    ).scalar_one()

    if user_orm.address.id != entity.address.id:
        old_address_id = user_orm.address.id
        update_address_statement = (
            update(UserORM)
            .where(UserORM.email == entity.email)
            .values(
                address_id=entity.address.id,
            )
        )
        session.execute(update_address_statement)

        delete_old_address_statement = delete(AddressORM).where(
            AddressORM.id == old_address_id
        )
        session.execute(delete_old_address_statement)


def update_sql_entities(*entities: _PERSISTENT_ENTITIES) -> None:

    with session_maker() as session:
        for entity in entities:
            _prepare_entity_for_update(entity, session)
        session.commit()


@singledispatch
def _prepare_entity_for_update(entity: Any, session: Session) -> None:
    raise ValueError(f"No update register for {type(entity).__name__}")


@_prepare_entity_for_update.register
def _(entity: TrialUser, session: Session) -> None:

    # A single joined table update is not supported
    # https://github.com/sqlalchemy/sqlalchemy/discussions/10128

    update_base_statement = (
        update(UserORM)
        .where(UserORM.email == entity.email)
        .values(
            name=entity.name,
            meals_per_week=entity.meals_per_week,
        )
    )
    session.execute(update_base_statement)

    update_child_statement = (
        update(TrialUserORM)
        .where(TrialUserORM.email == entity.email)
        .values(
            trial_end_date=entity.trial_end_date,
            discount_value=entity.discount_value,
        )
    )
    session.execute(update_child_statement)

    update_user_address(entity, session)


@_prepare_entity_for_update.register
def _(entity: StandardUser, session: Session) -> None:

    update_base_statement = (
        update(UserORM)
        .where(UserORM.email == entity.email)
        .values(
            name=entity.name,
            meals_per_week=entity.meals_per_week,
        )
    )
    session.execute(update_base_statement)

    update_user_address(entity, session)

from functools import singledispatch

from sqlalchemy import update, Update
from sqlalchemy.orm import Session

from .sql import session_maker
from .user import UserORM, TrialUser, TrialUserORM

_PERSISTENT_ENTITIES = TrialUser


def update_sql_entities(*entities: _PERSISTENT_ENTITIES) -> None:

    with session_maker() as session:
        for entity in entities:
            _prepare_entity_for_update(entity, session)
        session.commit()


@singledispatch
def _prepare_entity_for_update(trial_user: TrialUser, session: Session) -> None:

    # A single joined table update is not supported
    # https://github.com/sqlalchemy/sqlalchemy/discussions/10128

    update_base_statement = (
        update(UserORM)
        .where(UserORM.email == trial_user.email)
        .values(
            name=trial_user.name,
            meals_per_week=trial_user.meals_per_week,
        )
    )
    session.execute(update_base_statement)

    update_child_statement = (
        update(TrialUserORM)
        .where(TrialUserORM.email == trial_user.email)
        .values(
            trial_end_date=trial_user.trial_end_date,
            discount_value=trial_user.discount_value,
        )
    )
    session.execute(update_child_statement)

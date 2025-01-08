from abc import ABC, abstractmethod
from typing import override, Any

from sqlalchemy import select, Select

from .orm import handling_event_table
from .model import HandlingEvent
from ..sql import engine


class HandlingEventRepository(ABC):

    @classmethod
    @abstractmethod
    def get_from_id(self, id_: int) -> HandlingEvent | None: ...


class HandlingEventSqlRepository(HandlingEventRepository):

    @classmethod
    @override
    def get_from_id(self, id_: int) -> HandlingEvent | None:

        statement = select(handling_event_table).where(handling_event_table.c.id == id_)

        with engine.connect() as conn:
            handling_event_orm = conn.execute(statement).one_or_none()
            if handling_event_orm is None:
                return None

        return HandlingEvent(
            handling_event_orm.id,
            handling_event_orm.delivery_id,
            handling_event_orm.to_address_id,
            handling_event_orm.from_address_id,
            handling_event_orm.completion_time,
        )


def get_handling_event_repository() -> HandlingEventRepository:
    return HandlingEventSqlRepository()

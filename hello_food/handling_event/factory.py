from abc import ABC, abstractmethod
from typing import override, Any, Mapping

from sqlalchemy import insert

from .orm import handling_event_table
from .model import HandlingEvent
from ..mixins import JsonFactory
from ..sql import engine


class HandlingEventFactory(JsonFactory[HandlingEvent], ABC):

    @classmethod
    @abstractmethod
    def create_from_values(
        self,
        delivery_id: int,
        to_address_id: int,
        from_address_id: int,
        completion_time: int,
    ) -> HandlingEvent: ...


class HandlingEventSqlFactory(HandlingEventFactory):

    @classmethod
    @override
    def create_from_values(
        cls,
        delivery_id: int,
        to_address_id: int,
        from_address_id: int,
        completion_time: int,
    ) -> HandlingEvent:

        with engine.connect() as connection:
            statement = (
                insert(handling_event_table)
                .values(
                    delivery_id=delivery_id,
                    to_address_id=to_address_id,
                    from_address_id=from_address_id,
                    completion_time=completion_time,
                )
                .returning(handling_event_table.c.id)
            )
            handling_event_id = connection.execute(statement).scalar_one()
            connection.commit()

        return HandlingEvent(
            handling_event_id,
            delivery_id,
            to_address_id,
            from_address_id,
            completion_time,
        )

    @override
    @classmethod
    def create_from_json(cls, json_as_dict: Mapping[str, Any]) -> HandlingEvent:

        delivery_id = cls._parse_int_from_json(json_as_dict, "delivery_id")
        to_address_id = cls._parse_int_from_json(json_as_dict, "to_address_id")
        from_address_id = cls._parse_int_from_json(json_as_dict, "from_address_id")
        completion_time = cls._parse_int_from_json(json_as_dict, "completion_time")

        return cls.create_from_values(
            delivery_id,
            to_address_id,
            from_address_id,
            completion_time,
        )


def get_handling_event_factory() -> HandlingEventFactory:
    return HandlingEventSqlFactory()

from typing import Any, Mapping

from ..handling_event import get_handling_event_factory


def create_new_handling_event(handling_event_as_json_dict: Mapping[str, Any]) -> None:

    handling_event_factory = get_handling_event_factory()
    handling_event_factory.create_from_json(handling_event_as_json_dict)

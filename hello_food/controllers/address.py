from typing import Any, Mapping

from ..address import get_address_factory


def create_new_address(address_as_json_dict: Mapping[str, Any]) -> None:

    address_factory = get_address_factory()
    address_factory.create_from_json(address_as_json_dict)

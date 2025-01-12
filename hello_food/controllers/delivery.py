from typing import Any, Mapping

from ..util import parse_int_from_json
from ..update_driver import update_sql_entities
from ..delivery import get_delivery_factory, get_delivery_repository


def create_new_delivery(delivery_as_json_dict: Mapping[str, Any]) -> None:

    delivery_factory = get_delivery_factory()
    delivery_factory.create_from_json(delivery_as_json_dict)


def update_delivery_address(
    update_delivery_address_as_json_dict: Mapping[str, Any]
) -> None:

    new_address_id = parse_int_from_json(
        update_delivery_address_as_json_dict, "address_id"
    )
    delivery_id = parse_int_from_json(
        update_delivery_address_as_json_dict, "delivery_id"
    )

    delivery_repository = get_delivery_repository()
    delivery_to_update = delivery_repository.get_from_id(delivery_id)

    assert (
        delivery_to_update is not None
        and f"No delivery address found for id={delivery_id}"
    )

    # Set the new address
    delivery_to_update.address_id = new_address_id

    update_sql_entities(delivery_to_update)

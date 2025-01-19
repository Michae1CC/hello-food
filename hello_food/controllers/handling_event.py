from typing import Any, Mapping

from ..delivery import get_delivery_repository
from ..handling_event import (
    HandlingEvent,
    get_handling_event_factory,
    get_handling_event_repository,
)
from ..user import User, get_user_repository
from ..services import send_customer_email


def is_first_handling_event_for_delivery(delivery_id: int) -> bool:

    handling_event_repository = get_handling_event_repository()
    delivery_handling_events = handling_event_repository.get_from_delivery_id(
        delivery_id
    )
    print("Handling events")
    print(delivery_handling_events)

    return len(delivery_handling_events) == 1


def is_to_address_customer_address(handling_event: HandlingEvent, user: User) -> bool:

    return handling_event.to_address_id == user.address_id


def create_new_handling_event(handling_event_as_json_dict: Mapping[str, Any]) -> None:

    handling_event_factory = get_handling_event_factory()
    created_handling_event = handling_event_factory.create_from_json(
        handling_event_as_json_dict
    )

    delivery_event_repository = get_delivery_repository()
    handing_event_delivery = delivery_event_repository.get_from_id(
        created_handling_event.delivery_id
    )
    assert handing_event_delivery is not None and "No delivery found for handling event"

    user_repository = get_user_repository()
    handling_event_user = user_repository.get_from_id(handing_event_delivery.id)
    assert handling_event_user is not None and "No user found for handling event"

    if is_first_handling_event_for_delivery(created_handling_event.delivery_id):
        send_customer_email(handling_event_user.email, "Your order is on it's way!", "")

    if is_to_address_customer_address(created_handling_event, handling_event_user):
        send_customer_email(handling_event_user.email, "Your order is almost here!", "")

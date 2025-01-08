from typing import Any, Mapping

from ..user import get_standard_user_factory


def create_new_standard_user(standard_user_as_json_dict: Mapping[str, Any]) -> None:

    standard_user_factory = get_standard_user_factory()
    standard_user_factory.create_from_json(standard_user_as_json_dict)

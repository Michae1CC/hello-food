import time
from typing import Any, Mapping, TypeVar, cast

_T = TypeVar("_T", bound=int | float | str)


def get_current_unix_epoch() -> int:
    return int(time.time())


def get_attribute_from_json(
    json_as_dict: Mapping[str, Any], attribute_name: str
) -> Any:
    try:
        return json_as_dict[attribute_name]
    except KeyError as e:
        message = "Could not find attribute %s from provided JSON dict" % (
            attribute_name,
        )
        raise KeyError(message) from e


def parse_value_from_json(
    json_as_dict: Mapping[str, Any], attribute_name: str, type_: type[_T]
) -> _T:
    try:
        return cast(_T, type_(get_attribute_from_json(json_as_dict, attribute_name)))
    except ValueError as e:
        _CONVERT_FAILURE = "Could not convert attribute %s as %s"
        message = _CONVERT_FAILURE % (
            attribute_name,
            type_.__name__,
        )
        raise ValueError(message) from e


def parse_int_from_json(json_as_dict: Mapping[str, Any], attribute_name: str) -> int:
    return parse_value_from_json(json_as_dict, attribute_name, int)


def parse_float_from_json(
    json_as_dict: Mapping[str, Any], attribute_name: str
) -> float:
    return parse_value_from_json(json_as_dict, attribute_name, float)


def parse_str_from_json(json_as_dict: Mapping[str, Any], attribute_name: str) -> str:
    return parse_value_from_json(json_as_dict, attribute_name, str)

from abc import abstractmethod, ABC
from typing import Any, Self, TypeVar

_T = TypeVar("_T", bound=str)


class JsonFactory(ABC):
    _CONVERT_FAILURE = "Could not convert attribute %s as %s for class %s"

    @classmethod
    def _get_attribute_from_json(
        cls, json_as_dict: dict[str, Any], attribute_name: str
    ) -> Any:
        try:
            return json_as_dict[attribute_name]
        except KeyError as e:
            message = "Could not find attribute %s from provided JSON dict" % (
                attribute_name,
            )
            raise KeyError(message) from e

    @classmethod
    def _parse_int_from_json(
        cls, json_as_dict: dict[str, Any], attribute_name: str
    ) -> int:
        try:
            return int(cls._get_attribute_from_json(json_as_dict, attribute_name))
        except ValueError as e:
            message = cls._CONVERT_FAILURE % (
                attribute_name,
                int.__name__,
                cls.__name__,
            )
            raise ValueError(message) from e

    @classmethod
    def _parse_str_from_json(
        cls, json_as_dict: dict[str, Any], attribute_name: str
    ) -> str:
        try:
            return str(cls._get_attribute_from_json(json_as_dict, attribute_name))
        except ValueError as e:
            message = cls._CONVERT_FAILURE % (
                attribute_name,
                str.__name__,
                cls.__name__,
            )
            raise ValueError(message) from e

    @classmethod
    @abstractmethod
    def from_json(cls, json_as_dict: dict[str, Any]) -> Self: ...

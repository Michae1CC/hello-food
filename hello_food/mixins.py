from abc import abstractmethod, ABC
from typing import Any, Self, TypeVar, cast

_T = TypeVar("_T", bound=int | float | str)


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
    def _parse_value_from_json(
        cls, json_as_dict: dict[str, Any], attribute_name: str, type_: type[_T]
    ) -> _T:
        try:
            return cast(
                _T, type_(cls._get_attribute_from_json(json_as_dict, attribute_name))
            )
        except ValueError as e:
            message = cls._CONVERT_FAILURE % (
                attribute_name,
                type_.__name__,
                cls.__name__,
            )
            raise ValueError(message) from e

    @classmethod
    def _parse_int_from_json(
        cls, json_as_dict: dict[str, Any], attribute_name: str
    ) -> int:
        return cls._parse_value_from_json(json_as_dict, attribute_name, int)

    @classmethod
    def _parse_float_from_json(
        cls, json_as_dict: dict[str, Any], attribute_name: str
    ) -> float:
        return cls._parse_value_from_json(json_as_dict, attribute_name, float)

    @classmethod
    def _parse_str_from_json(
        cls, json_as_dict: dict[str, Any], attribute_name: str
    ) -> str:
        return cls._parse_value_from_json(json_as_dict, attribute_name, str)

    @classmethod
    @abstractmethod
    def from_json(cls, json_as_dict: dict[str, Any]) -> Self: ...

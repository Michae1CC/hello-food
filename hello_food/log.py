from __future__ import annotations

import logging
import logging.config
import sys
from typing import Optional
from typing import TypeVar
from typing import Literal

LOGGING_LEVELS = (
    Literal[50] | Literal[40] | Literal[30] | Literal[20] | Literal[10] | Literal[0]
)

_IT = TypeVar("_IT", bound="Identified")

logging.config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "loggers": {
            "app": {"level": "INFO", "handlers": ["wsgi"], "propagate": True},
        },
    }
)

# set initial level to WARN.  This so that
# log statements don't occur in the absence of explicit
# logging
rootlogger = logging.getLogger("hello_food")
if rootlogger.level == logging.NOTSET:
    rootlogger.setLevel(logging.WARN)


def _add_default_handler(logger: logging.Logger) -> None:
    """
    Sets a default logger handler to log to stdout. Also sets
    the logger format.
    """

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        # add json formatting here
        logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )
    logger.addHandler(handler)


def _qual_logger_name_for_cls(cls: type[Identified]) -> str:
    """
    Creates a qualified logger name for the provided class
    """

    return cls.__module__ + "." + cls.__name__


def class_logger(cls: type[_IT]) -> type[_IT]:
    logger = logging.getLogger(_qual_logger_name_for_cls(cls))
    cls._should_log_debug = lambda self: logger.isEnabledFor(  # type: ignore[method-assign]  # noqa: E501
        logging.DEBUG
    )
    cls._should_log_info = lambda self: logger.isEnabledFor(  # type: ignore[method-assign]  # noqa: E501
        logging.INFO
    )
    cls.logger = logger
    return cls


class Identified:

    _log_level: LOGGING_LEVELS

    logging_name: str | None = None

    logger: logging.Logger

    def _should_log_debug(self) -> bool:
        return self.logger.isEnabledFor(logging.DEBUG)

    def _should_log_info(self) -> bool:
        return self.logger.isEnabledFor(logging.INFO)


def instance_logger(instance: Identified, level: LOGGING_LEVELS) -> None:
    """create a logger for an instance that implements :class:`.Identified`."""

    instance._log_level = level

    if instance.logging_name:
        name = "%s.%s" % (
            _qual_logger_name_for_cls(instance.__class__),
            instance.logging_name,
        )
    else:
        name = _qual_logger_name_for_cls(instance.__class__)

    instance.logger = logging.getLogger(name)
    instance.logger.setLevel(level)
    _add_default_handler(instance.logger)


class logger_level_property:

    def __get__(
        self, instance: Optional[Identified], owner: type[Identified]
    ) -> LOGGING_LEVELS | logger_level_property:
        if instance is None:
            return self
        else:
            return instance._log_level

    def __set__(self, instance: Identified, value: LOGGING_LEVELS) -> None:
        instance_logger(instance, value)

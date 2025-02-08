import logging

from functools import wraps, singledispatch
from http import HTTPStatus
import sqlalchemy as sa
from typing import cast, Mapping, Callable, Literal, Any
from flask import request, Flask, Response, make_response

from .sql import engine, metadata
from .log import rootlogger
from .controllers.address import create_new_address
from .controllers.delivery import create_new_delivery, update_delivery_address
from .controllers.handling_event import create_new_handling_event
from .controllers.meal import create_new_meal
from .controllers.user import create_new_standard_user, create_new_trial_user


@singledispatch
def transform_handler_response(
    response: Any, response_status: HTTPStatus = HTTPStatus.OK
) -> Response:
    return make_response(response, response_status)


@transform_handler_response.register
def _(response: None, response_status: HTTPStatus = HTTPStatus.OK) -> Response:
    logging.info("Returned an empty response")
    return Response(status=HTTPStatus.NO_CONTENT)


@transform_handler_response.register
def _(response: dict, response_status: HTTPStatus = HTTPStatus.OK) -> Response:  # type: ignore
    return make_response(response, response_status)


@transform_handler_response.register
def _(response: Response, response_status: HTTPStatus = HTTPStatus.OK) -> Response:
    return response


def create_app() -> Flask:
    # create and configure the app
    flask_app = Flask(__name__, instance_relative_config=True)
    metadata.create_all(engine)

    # Default config
    flask_app.config.update(
        {
            "MAX_CONTENT_LENGTH": 1024**3,  # 1GB upload limit
            "TEMPLATES_AUTO_RELOAD": True,  # Reload templates from disk if they change
            "COMPRESS_MIN_SIZE": 1000,  # (kB) Don't waste time compressing small responses
        }
    )

    # Healthcheck
    @flask_app.route("/healthcheck")
    def healthcheck() -> Response:
        rootlogger.debug("healthcheck")

        # Test the db connection
        with engine.connect() as db_connection:
            db_connection.execute(sa.text("SELECT 1"))

        return make_response("PASSTEST3", HTTPStatus.OK)

    def attach_api(
        methods: list[
            Literal["GET"]
            | Literal["POST"]
            | Literal["DELETE"]
            | Literal["PATCH"]
            | Literal["OPTIONS"]
        ],
        resource: str,
        api_handler: Callable[[Mapping[str, Any]], Response | dict[str, Any] | None],
    ) -> None:
        @flask_app.route(resource, methods=methods)
        @wraps(api_handler)
        def decorator() -> Response:

            try:
                request_data = cast(Mapping[str, Any], request.json)
                handler_response = api_handler(request_data)
            except sa.exc.MultipleResultsFound as e:
                return make_response(
                    {
                        "reason": "Multiple responses returned from query.",
                        "error": str(e),
                    },
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                )
            except sa.exc.NoResultFound as e:
                return make_response(
                    {"error": str(e)},
                    HTTPStatus.NOT_FOUND,
                )
            except Exception as e:
                rootlogger.error(e)
                # Have a catch all for any exceptions generated by the routes.
                # Will be better to break this up a created specific responses/
                # actions for different exceptions.
                return make_response(
                    {"error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
                )

            return transform_handler_response(handler_response)

    # curl -i -X POST --header "Content-type: application/json" -d '{"unit":"U 19","street_name":"Green","suburb":"Morningside","postcode":"4171"}' http://127.0.0.1:5000/address/create
    attach_api(["POST"], "/address/create", create_new_address)

    attach_api(["POST"], "/delivery/create", create_new_delivery)
    attach_api(["POST"], "/delivery/update_address", update_delivery_address)

    attach_api(["POST"], "/handling_event/create", create_new_handling_event)

    attach_api(["POST"], "/meal/create", create_new_meal)

    attach_api(["POST"], "/standard_user/create", create_new_standard_user)
    attach_api(["POST"], "/trial_user/create", create_new_trial_user)

    return flask_app

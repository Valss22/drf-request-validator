from rest_framework.request import Request
from rest_framework.response import Response
from typing import TypedDict


class RequestBodyError(TypedDict):
    key_errors: list[str]
    type_errors: list[str]


detailed_errors: RequestBodyError = {}


def request_validator(schema: dict):
    def outer(func):
        def inner(request: Request):
            for (schema_key, schema_type_key), (data_key, data_value) in zip(
                schema.items(), request.data.items()
            ):
                if schema_key != data_key:
                    detailed_errors.update(
                        detailed_errors["key_errors"].append(
                            f"Field '{schema_key}' is expected, but '{data_key}' is recieved"
                        )
                    )
                if schema_type_key is not type(data_value):
                    detailed_errors.update(
                        detailed_errors["type_errors"].append(
                            f"It's expected the field '{schema_key}'"
                            + f"has the type {schema_type_key},"
                            + f"but recieved {type(data_value)}"
                        )
                    )
            if detailed_errors:
                return Response(detailed_errors)
            return func(request)

        return inner

    return outer

from rest_framework.request import Request
from rest_framework.response import Response
from typing import TypedDict
from .enums import ErrorMessage


class ErrorDetail(TypedDict):
    key: str
    msg: str
    detail: str


def request_validator(schema: dict):
    def outer(func):
        def inner(request: Request):

            error_details: list[ErrorDetail] = []
            copy_of_valid_req_data_keys = []

            for (schema_key, schema_type_key), (data_key, data_value) in zip(
                schema.items(), request.data.items()
            ):
                if schema_key != data_key:
                    error_details.append(
                        {
                            "key": data_key,
                            "msg": ErrorMessage.INVALID_KEY,
                            "detail": f"key '{schema_key}' is expected",
                        }
                    )
                    copy_of_valid_req_data_keys.append(schema_key)
                else:
                    copy_of_valid_req_data_keys.append(data_key)

                if schema_type_key is not type(data_value):
                    error_details.append(
                        {
                            "key": data_key,
                            "msg": ErrorMessage.TYPE,
                            "detail": f"It's expected has the type {schema_type_key}, but recieved {type(data_value)}",
                        }
                    )
            for schema_key in schema.keys():
                if schema_key not in copy_of_valid_req_data_keys:
                    error_details.append(
                        {
                            "msg": ErrorMessage.MISSING_KEY,
                            "detail": f"Missing key '{schema_key}'",
                        }
                    )
            if error_details:
                return Response(error_details)
            return func(request)

        return inner

    return outer

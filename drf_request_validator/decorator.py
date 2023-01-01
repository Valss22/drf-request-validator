from rest_framework.request import Request
from rest_framework.response import Response
from typing import TypedDict


class ErrorDetail(TypedDict):
    field: str
    msg: str
    detail: str


error_details: list[ErrorDetail] = []


def request_validator(schema: dict):
    def outer(func):
        def inner(request: Request):
            for (schema_key, schema_type_key), (data_key, data_value) in zip(
                schema.items(), request.data.items()
            ):
                if schema_key != data_key:
                    error_detail: ErrorDetail = {}
                    error_detail["field"] = data_key
                    error_detail["msg"] = "field name error"
                    error_detail["detail"] = f"'{schema_key}' is expected"
                    error_details.append(error_detail)

                if schema_type_key is not type(data_value):
                    error_detail: ErrorDetail = {}
                    error_detail["field"] = data_key
                    error_detail["msg"] = "field value type error"
                    error_detail[
                        "detail"
                    ] = f"It's expected has the type {schema_type_key}, but recieved {type(data_value)}"
                    error_details.append(error_detail)

            if error_details:
                return Response(error_details)
            return func(request)

        return inner

    return outer

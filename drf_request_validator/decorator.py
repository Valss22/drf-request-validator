from rest_framework.request import Request
from rest_framework.response import Response
from typing import TypedDict
from .enums import ErrorMessage


class ErrorDetail(TypedDict):
    key: str
    msg: str


def request_validator(schema: dict):
    def outer(func):
        def inner(request: Request):

            error_details: list[ErrorDetail] = []

            for req_key, req_value in request.data.items():
                if req_key not in list(schema.keys()):
                    error_details.append(
                        ErrorDetail(key=req_key, msg=ErrorMessage.INVALID_KEY)
                    )
                else:
                    if schema[req_key] is not type(req_value):
                        error_details.append(
                            ErrorDetail(key=req_key, msg=ErrorMessage.INVALID_TYPE)
                        )
            if error_details:
                return Response(error_details)
            return func(request)

        return inner

    return outer

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

            for req_key in request.data.keys():
                if req_key not in list(schema.keys()):
                    error_details.append(
                        ErrorDetail(key=req_key, msg=ErrorMessage.INVALID_KEY)
                    )

            if error_details:
                return Response(error_details)
            return func(request)

        return inner

    return outer

from rest_framework.request import Request
from rest_framework.response import Response
from drf_request_validator.types import ErrorMessage, ErrorDetail


def validation_iteration(req_data: dict, schema_data: dict, error_details: list):
    for req_key, req_value in req_data.items():
        if req_key not in list(schema_data.keys()):
            error_details.append(ErrorDetail(key=req_key, msg=ErrorMessage.INVALID_KEY))
        else:
            if type(schema_data[req_key]) is dict:
                validation_iteration(
                    req_data[req_key], schema_data[req_key], error_details
                )
                continue
            if type(schema_data[req_key]) is list:
                ...
            if schema_data[req_key] is not type(req_value):
                error_details.append(
                    ErrorDetail(
                        key=req_key,
                        msg=ErrorMessage.INVALID_TYPE,
                        detail=f"type {schema_data[req_key]} is expected",
                    )
                )


def request_validator(schema: dict):
    def outer(func):
        def inner(request: Request):

            error_details: list[ErrorDetail] = []
            validation_iteration(request.data, schema, error_details)

            if error_details:
                return Response(error_details)
            return func(request)

        return inner

    return outer

from rest_framework.request import Request
from rest_framework.response import Response
from drf_request_validator.types import ErrorMessage, ErrorDetail


def list_validation(req_data: list, schema_data: list, error_details: list):
    for req_list_item in req_data:
        if type(schema_data[0]) is dict:
            if type(req_list_item) is dict:
                dict_validation(
                    req_list_item,
                    schema_data[0],
                    error_details,
                )
                continue
            else:
                error_details.append(
                    ErrorDetail(
                        msg=ErrorMessage.INVALID_TYPE,
                        detail=f"type {schema_data[0]} is expected",
                    )
                )
                continue
        else:
            if type(req_list_item) is not schema_data[0]:
                error_details.append(
                    ErrorDetail(
                        msg=ErrorMessage.INVALID_TYPE,
                        detail=f"type {schema_data[0]} is expected",
                    )
                )


def dict_validation(req_data: dict, schema_data: dict, error_details: list):
    for req_key, req_value in req_data.items():
        if req_key not in list(schema_data.keys()):
            error_details.append(ErrorDetail(key=req_key, msg=ErrorMessage.INVALID_KEY))
        else:
            if type(schema_data[req_key]) is dict:
                if type(req_data[req_key]) is dict:
                    dict_validation(
                        req_data[req_key], schema_data[req_key], error_details
                    )
                    continue
                else:
                    error_details.append(
                        ErrorDetail(
                            key=req_key,
                            msg=ErrorMessage.INVALID_TYPE,
                            detail=f"type {schema_data[req_key]} is expected",
                        )
                    )
                    continue
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
            if type(request.data) is list:
                list_validation(request.data, schema, error_details)
            else:
                dict_validation(request.data, schema, error_details)

            if error_details:
                return Response(error_details)
            return func(request)

        return inner

    return outer

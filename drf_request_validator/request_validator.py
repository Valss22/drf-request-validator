from rest_framework.request import Request
from rest_framework.response import Response


def request_validator(schema: dict):
    def outer(func):
        def inner(request: Request):
            for (schema_key, schema_type_key), (data_key, data_value) in zip(
                schema.items(), request.data.items()
            ):
                if schema_key != data_key:
                    return Response(
                        {
                            "msg": "Request body validation error, "
                            + f"expected {schema_key}, but recieved {data_key}"
                        }
                    )
                if schema_type_key is not type(data_value):
                    return Response(
                        {
                            "msg": "Request body validation error, "
                            + f"expected {schema_type_key}, but recieved {type(data_value)}"
                        }
                    )
            return func(request)

        return inner

    return outer

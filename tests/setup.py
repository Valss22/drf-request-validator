from drf_request_validator.types import ErrorMessage


def invalid_key_response(key: str) -> dict:
    return {"key": key, "msg": ErrorMessage.INVALID_KEY}


def invalid_type_response(key: str, expected_key_type) -> dict:
    return {
        "key": key,
        "msg": ErrorMessage.INVALID_TYPE,
        "detail": f"type {expected_key_type} is expected",
    }


schema = {"name": str, "age": int}

test_data = [
    (schema, {"name": "Vlad", "age": 20}, {"name": "Vlad", "age": 20}),
    (schema, {"naame": "Rudolf", "age": 21}, [invalid_key_response("naame")]),
    (schema, {"name": "Ruslan", "age": "twenty"}, [invalid_type_response("age", int)]),
    (
        schema,
        {"naame": "Danila", "age": "twenty"},
        [invalid_key_response("naame"), invalid_type_response("age", int)],
    ),
    (
        schema,
        {"naame": "Sergej", "agge": 20},
        [invalid_key_response("naame"), invalid_key_response("agge")],
    ),
]

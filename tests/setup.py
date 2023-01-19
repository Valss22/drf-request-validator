from drf_request_validator.types import ErrorMessage


def invalid_key_response(key: str) -> dict:
    return {"key": key, "msg": ErrorMessage.INVALID_KEY}


def invalid_type_response(key: str, expected_key_type) -> dict:
    return {
        "key": key,
        "msg": ErrorMessage.INVALID_TYPE,
        "detail": f"type {expected_key_type} is expected",
    }


success_response = {"msg": "ok"}

schema = {"name": str, "age": int}
schema2 = {"name": str, "age": {"month": int, "year": int}}
schema3 = [{"name": str, "age": int}]
schema4 = [str]
schema5 = {"items": [{"name": str, "age": int}]}
schema6 = {"object": {"object": {"numbers": [int]}}}

test_data = [
    (schema, {"name": "Vlad", "age": 20}, success_response),
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
    (
        schema2,
        {"name": "Igor", "age": {"month": 7, "year": 2000}},
        success_response,
    ),
    (
        schema2,
        {"age": {"mnth": "seven", "year": "two"}, "naame": "Igor"},
        [
            invalid_key_response("mnth"),
            invalid_type_response("year", int),
            invalid_key_response("naame"),
        ],
    ),
    (
        schema2,
        {"name": "Roman", "age": 18},
        [invalid_type_response("age", {"month": int, "year": int})],
    ),
    (
        schema3,
        [{"name": "Vlad", "age": 20}, {"name": "Sergej", "age": 21}],
        success_response,
    ),
    (schema3, {"name": "Dacha"}, [invalid_type_response("request.data", schema3)]),
    (
        schema3,
        [{"nme": "Vlad", "age": 20}, {"naame": "Sergej", "age": "twenty"}],
        [
            invalid_key_response("nme"),
            invalid_key_response("naame"),
            invalid_type_response("age", int),
        ],
    ),
    (schema4, ["a", "b"], success_response),
    (schema4, ["a", 3], [invalid_type_response("request.data", schema4)]),
    (schema5, {"items": [{"name": "Vladick", "age": 20}]}, success_response),
    (
        schema5,
        {"items": [{"nma": "Hui", "age": "dva"}]},
        [invalid_key_response("nma"), invalid_type_response("age", int)],
    ),
    (
        schema5,
        {"items": {"nma": "Hui", "age": "dva"}},
        [invalid_type_response("items", schema5["items"])],
    ),
    (schema6, {"objec": {"object": [1, 2, 3]}}, [invalid_key_response("objec")]),
    (
        schema6,
        {"object": {"object": [1, 2, 3]}},
        [invalid_type_response("object", {"numbers": [int]})],
    ),
    (
        schema6,
        {"object": {"object": {"numbers": ["a", "b"]}}},
        [invalid_type_response("numbers", [int])],
    ),
]

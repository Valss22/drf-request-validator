from drf_request_validator.types import ErrorMessage


schema = {"name": str, "age": int}

correct_request_data = {"name": "Vlad", "age": 20}
correct_response = {**correct_request_data}

invalid_key_request_data = {"name": "Vlad", "agge": 20}
invalid_key_response = [{"key": "agge", "msg": ErrorMessage.INVALID_KEY}]

invalid_type_request_data = {"name": "Vlad", "age": "twenty"}
invalid_type_response = [
    {
        "key": "age",
        "msg": ErrorMessage.INVALID_TYPE,
        "detail": f"type {int} is expected",
    }
]

test_data = [
    (schema, correct_request_data, correct_response),
    (schema, invalid_key_request_data, invalid_key_response),
    (schema, invalid_type_request_data, invalid_type_response),
]

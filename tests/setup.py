from drf_request_validator.types import ErrorMessage


schema = {"name": str, "age": int}

correct_request_data = {"name": "Vlad", "age": 20}
correct_response = {**correct_request_data}

invalid_key_request_data = {"naame": "Vlad", "age": 20}
invalid_key_response = [{"key": "naame", "msg": ErrorMessage.INVALID_KEY}]

invalid_type_request_data = {"name": "Vlad", "age": "twenty"}
invalid_type_response = [
    {
        "key": "age",
        "msg": ErrorMessage.INVALID_TYPE,
        "detail": f"type {int} is expected",
    }
]

invalid_key_and_type_request_data = {"naame": "Danila", "age": "twenty"}
invalid_key_and_type_response = [invalid_key_response[0], invalid_type_response[0]]

test_data = [
    (schema, correct_request_data, correct_response),
    (schema, invalid_key_request_data, invalid_key_response),
    (schema, invalid_type_request_data, invalid_type_response),
    (schema, invalid_key_and_type_request_data, invalid_key_and_type_response),
]

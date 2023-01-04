from drf_request_validator import request_validator
from drf_request_validator import decorator
from drf_request_validator.enums import ErrorMessage
from pytest import MonkeyPatch
import pytest


class MockRequest:
    def __init__(self, data: dict) -> None:
        self.data = data


def mock_response(data: dict | list) -> dict:
    return data


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


@pytest.mark.parametrize("schema,request_data,response", test_data)
def test_decorator(schema, request_data, response, monkeypatch: MonkeyPatch):
    monkeypatch.setattr(decorator, "Response", mock_response)

    @request_validator(schema)
    def mock_http_handler(request=MockRequest(request_data)) -> mock_response:
        return mock_response(request.data)

    print(mock_http_handler(MockRequest(request_data)))
    assert mock_http_handler(MockRequest(request_data)) == response

from drf_request_validator import request_validator
from drf_request_validator import decorator
from pytest import MonkeyPatch
import pytest


class MockRequest:
    def __init__(self, data: dict) -> None:
        self.data = data


def mock_response(data: dict | list) -> dict:
    return data


SCHEMA = {"name": str, "age": int}

CORRECT_REQUEST_DATA = {"name": "Vlad", "age": 20}
CORRECT_RESPONSE = {**CORRECT_REQUEST_DATA}

UNCORRECT_KEY_REQUEST_DATA = {"name": "Vlad", "agge": 20}
UNCORRECT_KEY_RESPONSE = [
    {"field": "agge", "msg": "field name error", "detail": "'age' is expected"}
]

UNCORRECT_TYPE_REQUEST_DATA = {"name": "Vlad", "age": "twenty"}
UNCORRECT_TYPE_RESPONSE = {
    "errors": [f"It's expected the field 'age' has the type {int}, but recieved {str}"]
}

# MISSING_KEY_REQUEST_DATA = {"name": "Danila"}
# MISSING_KEY_RESPONSE = {**MISSING_KEY_REQUEST_DATA}

TEST_DATA = [
    (SCHEMA, CORRECT_REQUEST_DATA, CORRECT_RESPONSE),
    (SCHEMA, UNCORRECT_KEY_REQUEST_DATA, UNCORRECT_KEY_RESPONSE),
    (SCHEMA, UNCORRECT_TYPE_REQUEST_DATA, UNCORRECT_TYPE_RESPONSE),
    # (SCHEMA, MISSING_KEY_REQUEST_DATA, MISSING_KEY_RESPONSE),
]


@pytest.mark.parametrize("schema,request_data,response", TEST_DATA)
def test_decorator(schema, request_data, response, monkeypatch: MonkeyPatch):
    monkeypatch.setattr(decorator, "Response", mock_response)

    @request_validator(schema)
    def mock_http_handler(request=MockRequest(request_data)) -> mock_response:
        return mock_response(request.data)

    assert mock_http_handler(MockRequest(request_data)) == response

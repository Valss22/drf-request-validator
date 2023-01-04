from drf_request_validator import request_validator
from drf_request_validator import decorator
from .setup import test_data
from pytest import MonkeyPatch
import pytest


class MockRequest:
    def __init__(self, data: dict) -> None:
        self.data = data


def mock_response(data: dict | list) -> dict:
    return data


@pytest.mark.parametrize("schema,request_data,response", test_data)
def test_decorator(schema, request_data, response, monkeypatch: MonkeyPatch):
    monkeypatch.setattr(decorator, "Response", mock_response)

    @request_validator(schema)
    def mock_http_handler(request=MockRequest(request_data)) -> mock_response:
        return mock_response(request.data)

    print(mock_http_handler(MockRequest(request_data)))
    assert mock_http_handler(MockRequest(request_data)) == response

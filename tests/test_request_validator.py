from drf_request_validator import request_validator
from drf_request_validator import main
from pytest import MonkeyPatch


class MockRequest:
    def __init__(self, data: dict) -> None:
        self.data = data


def mock_response(data: dict) -> dict:
    return data


schema = {"name": str, "age": int}
request_data = {"name": "Vlad", "age": 20}


def test_request_example(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(main, "Response", mock_response)

    @request_validator(schema)
    def mock_http_handler(request=MockRequest(request_data)) -> mock_response:
        return mock_response(request.data)

    assert mock_http_handler(MockRequest(request_data)) == mock_response(request_data)

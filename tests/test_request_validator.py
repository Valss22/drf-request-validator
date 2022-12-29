class MockRequest:
    def __init__(self, data: dict) -> None:
        self.data = data


def test_request_example():
    request = MockRequest({})
    assert request.data == {}

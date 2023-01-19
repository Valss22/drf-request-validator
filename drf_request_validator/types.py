from enum import Enum
from typing import TypedDict


class BaseEnum(str, Enum):
    def __str__(self):
        return self.value


class ErrorMessage(BaseEnum):
    INVALID_KEY = "invalid key"
    MISSING_KEY = "missing key"
    INVALID_TYPE = "invalid type"


class ErrorDetail(TypedDict):
    key: str
    msg: str
    detail: str

from enum import Enum


class BaseEnum(str, Enum):
    def __str__(self):
        return self.value


class ErrorMessage(BaseEnum):
    INVALID_KEY = "invalid key"
    TYPE = "type error"
    MISSING_KEY = "missing key"

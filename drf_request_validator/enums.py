from enum import Enum


class BaseEnum(str, Enum):
    def __str__(self):
        return self.value


class ErrorMessage(BaseEnum):
    INVALID_KEY = "invalid key"
    INVALID_TYPE = "invalid type"
    MISSING_KEY = "missing key"
    EXTRA_KEY = "extra key"

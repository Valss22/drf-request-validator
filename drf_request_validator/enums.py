from enum import Enum


class BaseEnum(str, Enum):
    def __str__(self):
        return self.value


class ErrorMessage(BaseEnum):
    KEY = "key error"
    TYPE = "type error"

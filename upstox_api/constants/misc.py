from enum import Enum


class Misc(Enum):
    BASE_MODULE_NAME = "upstox_api.api"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


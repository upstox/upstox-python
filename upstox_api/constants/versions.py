from enum import Enum

class Versions(Enum):
    DEFAULT = "DEFAULT"
    Version_2_0_0 = "2.0.0"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


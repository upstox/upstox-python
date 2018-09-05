from enum import Enum

class Versions(Enum):
    DEFAULT = "DEFAULT"
    Version_1_5_6 = "1.5.6"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


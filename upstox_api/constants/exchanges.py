from enum import Enum


class Exchanges(Enum):
    NSE_INDEX = "NSE_INDEX"
    NSE_EQ = "NSE_EQ"
    NCD_FO = "NCD_FO"
    NSE_FO = "NSE_FO"

    BSE_INDEX = "BSE_INDEX"
    BSE_EQ = "BSE_EQ"
    BCD_FO = "BCD_FO"
    BSE_FO = "BSE_FO"

    MCX_FO = "MCX_FO"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


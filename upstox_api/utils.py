from collections import namedtuple
import re

Instrument = namedtuple('Instrument', ['exchange', 'token', 'parent_token', 'symbol',
                                       'name', 'closing_price', 'expiry', 'strike_price',
                                       'tick_size', 'lot_size', 'instrument_type', 'isin'])


class CustomEnum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
    def __setattr__(self, name, value):
        raise RuntimeError("Cannot override values")
    def __delattr__(self, name):
        raise RuntimeError("Cannot delete values")


class PyCurlVerbs(CustomEnum):
    PUT = 'PUT'
    DELETE = 'DELETE'
    GET = 'GET'
    POST = 'POST'


class OHLCInterval(CustomEnum):
    Minute_1 = '1MINUTE'
    Minute_5 = '5MINUTE'
    Minute_10 = '10MINUTE'
    Minute_30 = '30MINUTE'
    Minute_60 = '60MINUTE'
    Day_1 = '1DAY'
    Week_1 = '1WEEK'
    Month_1 = '1MONTH'

    @staticmethod
    def parse(str):
        str = str.upper()
        if str == '1MINUTE':
            return OHLCInterval.Minute_1
        if str == '5MINUTE':
            return OHLCInterval.Minute_5
        if str == '10MINUTE':
            return OHLCInterval.Minute_10
        if str == '30MINUTE':
            return OHLCInterval.Minute_30
        if str == '60MINUTE':
            return OHLCInterval.Minute_60
        if str == '1DAY':
            return OHLCInterval.Day_1
        if str == '1WEEK':
            return OHLCInterval.Week_1
        if str == '1MONTH':
            return OHLCInterval.Month_1
        return None


class TransactionType(CustomEnum):
    Buy = 'B'
    Sell = 'S'

    @staticmethod
    def parse(str):
        str = str.upper()
        if str == 'B':
            return TransactionType.Buy
        if str == 'S':
            return TransactionType.Sell
        return None


class OrderType(CustomEnum):
    Market = 'M'
    Limit = 'L'
    StopLossLimit = 'SL'
    StopLossMarket = 'SL-M'

    @staticmethod
    def parse(str):
        str = str.upper()
        if str == 'M':
            return OrderType.Market
        if str == 'L':
            return OrderType.Limit
        if str == 'SL':
            return OrderType.StopLossLimit
        if str == 'SL-M':
            return OrderType.StopLossMarket
        return None

class ProductType(CustomEnum):
    Intraday = 'I'
    Delivery = 'D'
    CoverOrder = 'CO'
    OneCancelsOther = 'OCO'

    @staticmethod
    def parse(str):
        str = str.upper()
        if str == 'I':
            return ProductType.Intraday
        if str == 'D':
            return ProductType.Delivery
        if str == 'CO':
            return ProductType.CoverOrder
        if str == 'OCO':
            return ProductType.OneCancelsOther
        return None


class DurationType(CustomEnum):
    DAY = 'DAY'
    IOC = 'IOC'

    @staticmethod
    def parse(str):
        str = str.upper()
        if str == 'DAY':
            return DurationType.DAY
        if str == 'IOC':
            return DurationType.IOC
        return None


class LiveFeedType(CustomEnum):
    LTP = 'LTP'
    Full = 'Full'

    @staticmethod
    def parse(str):
        str = str.upper()
        if str == 'LTP':
            return LiveFeedType.LTP
        if str == 'FULL':
            return LiveFeedType.Full
        return None


def is_status_2xx(code):
    return re.search('^2', str(code)) is not None
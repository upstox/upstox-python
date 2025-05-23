# coding: utf-8

"""
    Upstox Developer API

    Build your App on the Upstox platform  ![Banner](https://api.upstox.com/api-docs/images/banner.jpg \"banner\")  # Introduction  Upstox API is a set of rest APIs that provide data required to build a complete investment and trading platform. Execute orders in real time, manage user portfolio, stream live market data (using Websocket), and more, with the easy to understand API collection.  All requests are over HTTPS and the requests are sent with the content-type ‘application/json’. Developers have the option of choosing the response type as JSON or CSV for a few API calls.  To be able to use these APIs you need to create an App in the Developer Console and generate your **apiKey** and **apiSecret**. You can use a redirect URL which will be called after the login flow.  If you are a **trader**, you can directly create apps from Upstox mobile app or the desktop platform itself from **Apps** sections inside the **Account** Tab. Head over to <a href=\"http://account.upstox.com/developer/apps\" target=\"_blank\">account.upstox.com/developer/apps</a>.</br> If you are a **business** looking to integrate Upstox APIs, reach out to us and we will get a custom app created for you in no time.  It is highly recommended that you do not embed the **apiSecret** in your frontend app. Create a remote backend which does the handshake on behalf of the frontend app. Marking the apiSecret in the frontend app will make your app vulnerable to threats and potential issues.   # noqa: E501

    OpenAPI spec version: v2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class MarketQuoteSymbol(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'ohlc': 'Ohlc',
        'depth': 'DepthMap',
        'timestamp': 'str',
        'instrument_token': 'str',
        'symbol': 'str',
        'last_price': 'float',
        'volume': 'int',
        'average_price': 'float',
        'oi': 'float',
        'net_change': 'float',
        'total_buy_quantity': 'float',
        'total_sell_quantity': 'float',
        'lower_circuit_limit': 'float',
        'upper_circuit_limit': 'float',
        'last_trade_time': 'str',
        'oi_day_high': 'float',
        'oi_day_low': 'float'
    }

    attribute_map = {
        'ohlc': 'ohlc',
        'depth': 'depth',
        'timestamp': 'timestamp',
        'instrument_token': 'instrument_token',
        'symbol': 'symbol',
        'last_price': 'last_price',
        'volume': 'volume',
        'average_price': 'average_price',
        'oi': 'oi',
        'net_change': 'net_change',
        'total_buy_quantity': 'total_buy_quantity',
        'total_sell_quantity': 'total_sell_quantity',
        'lower_circuit_limit': 'lower_circuit_limit',
        'upper_circuit_limit': 'upper_circuit_limit',
        'last_trade_time': 'last_trade_time',
        'oi_day_high': 'oi_day_high',
        'oi_day_low': 'oi_day_low'
    }

    def __init__(self, ohlc=None, depth=None, timestamp=None, instrument_token=None, symbol=None, last_price=None, volume=None, average_price=None, oi=None, net_change=None, total_buy_quantity=None, total_sell_quantity=None, lower_circuit_limit=None, upper_circuit_limit=None, last_trade_time=None, oi_day_high=None, oi_day_low=None):  # noqa: E501
        """MarketQuoteSymbol - a model defined in Swagger"""  # noqa: E501
        self._ohlc = None
        self._depth = None
        self._timestamp = None
        self._instrument_token = None
        self._symbol = None
        self._last_price = None
        self._volume = None
        self._average_price = None
        self._oi = None
        self._net_change = None
        self._total_buy_quantity = None
        self._total_sell_quantity = None
        self._lower_circuit_limit = None
        self._upper_circuit_limit = None
        self._last_trade_time = None
        self._oi_day_high = None
        self._oi_day_low = None
        self.discriminator = None
        if ohlc is not None:
            self.ohlc = ohlc
        if depth is not None:
            self.depth = depth
        if timestamp is not None:
            self.timestamp = timestamp
        if instrument_token is not None:
            self.instrument_token = instrument_token
        if symbol is not None:
            self.symbol = symbol
        if last_price is not None:
            self.last_price = last_price
        if volume is not None:
            self.volume = volume
        if average_price is not None:
            self.average_price = average_price
        if oi is not None:
            self.oi = oi
        if net_change is not None:
            self.net_change = net_change
        if total_buy_quantity is not None:
            self.total_buy_quantity = total_buy_quantity
        if total_sell_quantity is not None:
            self.total_sell_quantity = total_sell_quantity
        if lower_circuit_limit is not None:
            self.lower_circuit_limit = lower_circuit_limit
        if upper_circuit_limit is not None:
            self.upper_circuit_limit = upper_circuit_limit
        if last_trade_time is not None:
            self.last_trade_time = last_trade_time
        if oi_day_high is not None:
            self.oi_day_high = oi_day_high
        if oi_day_low is not None:
            self.oi_day_low = oi_day_low

    @property
    def ohlc(self):
        """Gets the ohlc of this MarketQuoteSymbol.  # noqa: E501


        :return: The ohlc of this MarketQuoteSymbol.  # noqa: E501
        :rtype: Ohlc
        """
        return self._ohlc

    @ohlc.setter
    def ohlc(self, ohlc):
        """Sets the ohlc of this MarketQuoteSymbol.


        :param ohlc: The ohlc of this MarketQuoteSymbol.  # noqa: E501
        :type: Ohlc
        """

        self._ohlc = ohlc

    @property
    def depth(self):
        """Gets the depth of this MarketQuoteSymbol.  # noqa: E501


        :return: The depth of this MarketQuoteSymbol.  # noqa: E501
        :rtype: DepthMap
        """
        return self._depth

    @depth.setter
    def depth(self, depth):
        """Sets the depth of this MarketQuoteSymbol.


        :param depth: The depth of this MarketQuoteSymbol.  # noqa: E501
        :type: DepthMap
        """

        self._depth = depth

    @property
    def timestamp(self):
        """Gets the timestamp of this MarketQuoteSymbol.  # noqa: E501

        Time in milliseconds at which the feeds was updated  # noqa: E501

        :return: The timestamp of this MarketQuoteSymbol.  # noqa: E501
        :rtype: str
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this MarketQuoteSymbol.

        Time in milliseconds at which the feeds was updated  # noqa: E501

        :param timestamp: The timestamp of this MarketQuoteSymbol.  # noqa: E501
        :type: str
        """

        self._timestamp = timestamp

    @property
    def instrument_token(self):
        """Gets the instrument_token of this MarketQuoteSymbol.  # noqa: E501

        Key issued by Upstox for the instrument  # noqa: E501

        :return: The instrument_token of this MarketQuoteSymbol.  # noqa: E501
        :rtype: str
        """
        return self._instrument_token

    @instrument_token.setter
    def instrument_token(self, instrument_token):
        """Sets the instrument_token of this MarketQuoteSymbol.

        Key issued by Upstox for the instrument  # noqa: E501

        :param instrument_token: The instrument_token of this MarketQuoteSymbol.  # noqa: E501
        :type: str
        """

        self._instrument_token = instrument_token

    @property
    def symbol(self):
        """Gets the symbol of this MarketQuoteSymbol.  # noqa: E501

        Shows the trading symbol of the instrument  # noqa: E501

        :return: The symbol of this MarketQuoteSymbol.  # noqa: E501
        :rtype: str
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        """Sets the symbol of this MarketQuoteSymbol.

        Shows the trading symbol of the instrument  # noqa: E501

        :param symbol: The symbol of this MarketQuoteSymbol.  # noqa: E501
        :type: str
        """

        self._symbol = symbol

    @property
    def last_price(self):
        """Gets the last_price of this MarketQuoteSymbol.  # noqa: E501

        The last traded price of symbol  # noqa: E501

        :return: The last_price of this MarketQuoteSymbol.  # noqa: E501
        :rtype: float
        """
        return self._last_price

    @last_price.setter
    def last_price(self, last_price):
        """Sets the last_price of this MarketQuoteSymbol.

        The last traded price of symbol  # noqa: E501

        :param last_price: The last_price of this MarketQuoteSymbol.  # noqa: E501
        :type: float
        """

        self._last_price = last_price

    @property
    def volume(self):
        """Gets the volume of this MarketQuoteSymbol.  # noqa: E501

        The volume traded today on symbol  # noqa: E501

        :return: The volume of this MarketQuoteSymbol.  # noqa: E501
        :rtype: int
        """
        return self._volume

    @volume.setter
    def volume(self, volume):
        """Sets the volume of this MarketQuoteSymbol.

        The volume traded today on symbol  # noqa: E501

        :param volume: The volume of this MarketQuoteSymbol.  # noqa: E501
        :type: int
        """

        self._volume = volume

    @property
    def average_price(self):
        """Gets the average_price of this MarketQuoteSymbol.  # noqa: E501

        Average price  # noqa: E501

        :return: The average_price of this MarketQuoteSymbol.  # noqa: E501
        :rtype: float
        """
        return self._average_price

    @average_price.setter
    def average_price(self, average_price):
        """Sets the average_price of this MarketQuoteSymbol.

        Average price  # noqa: E501

        :param average_price: The average_price of this MarketQuoteSymbol.  # noqa: E501
        :type: float
        """

        self._average_price = average_price

    @property
    def oi(self):
        """Gets the oi of this MarketQuoteSymbol.  # noqa: E501

        Total number of outstanding contracts held by market participants exchange-wide (only F&O)  # noqa: E501

        :return: The oi of this MarketQuoteSymbol.  # noqa: E501
        :rtype: float
        """
        return self._oi

    @oi.setter
    def oi(self, oi):
        """Sets the oi of this MarketQuoteSymbol.

        Total number of outstanding contracts held by market participants exchange-wide (only F&O)  # noqa: E501

        :param oi: The oi of this MarketQuoteSymbol.  # noqa: E501
        :type: float
        """

        self._oi = oi

    @property
    def net_change(self):
        """Gets the net_change of this MarketQuoteSymbol.  # noqa: E501

        The absolute change from yesterday's close to last traded price  # noqa: E501

        :return: The net_change of this MarketQuoteSymbol.  # noqa: E501
        :rtype: float
        """
        return self._net_change

    @net_change.setter
    def net_change(self, net_change):
        """Sets the net_change of this MarketQuoteSymbol.

        The absolute change from yesterday's close to last traded price  # noqa: E501

        :param net_change: The net_change of this MarketQuoteSymbol.  # noqa: E501
        :type: float
        """

        self._net_change = net_change

    @property
    def total_buy_quantity(self):
        """Gets the total_buy_quantity of this MarketQuoteSymbol.  # noqa: E501

        The total number of bid quantity available for trading  # noqa: E501

        :return: The total_buy_quantity of this MarketQuoteSymbol.  # noqa: E501
        :rtype: float
        """
        return self._total_buy_quantity

    @total_buy_quantity.setter
    def total_buy_quantity(self, total_buy_quantity):
        """Sets the total_buy_quantity of this MarketQuoteSymbol.

        The total number of bid quantity available for trading  # noqa: E501

        :param total_buy_quantity: The total_buy_quantity of this MarketQuoteSymbol.  # noqa: E501
        :type: float
        """

        self._total_buy_quantity = total_buy_quantity

    @property
    def total_sell_quantity(self):
        """Gets the total_sell_quantity of this MarketQuoteSymbol.  # noqa: E501

        The total number of ask quantity available for trading  # noqa: E501

        :return: The total_sell_quantity of this MarketQuoteSymbol.  # noqa: E501
        :rtype: float
        """
        return self._total_sell_quantity

    @total_sell_quantity.setter
    def total_sell_quantity(self, total_sell_quantity):
        """Sets the total_sell_quantity of this MarketQuoteSymbol.

        The total number of ask quantity available for trading  # noqa: E501

        :param total_sell_quantity: The total_sell_quantity of this MarketQuoteSymbol.  # noqa: E501
        :type: float
        """

        self._total_sell_quantity = total_sell_quantity

    @property
    def lower_circuit_limit(self):
        """Gets the lower_circuit_limit of this MarketQuoteSymbol.  # noqa: E501

        The lower circuit of symbol  # noqa: E501

        :return: The lower_circuit_limit of this MarketQuoteSymbol.  # noqa: E501
        :rtype: float
        """
        return self._lower_circuit_limit

    @lower_circuit_limit.setter
    def lower_circuit_limit(self, lower_circuit_limit):
        """Sets the lower_circuit_limit of this MarketQuoteSymbol.

        The lower circuit of symbol  # noqa: E501

        :param lower_circuit_limit: The lower_circuit_limit of this MarketQuoteSymbol.  # noqa: E501
        :type: float
        """

        self._lower_circuit_limit = lower_circuit_limit

    @property
    def upper_circuit_limit(self):
        """Gets the upper_circuit_limit of this MarketQuoteSymbol.  # noqa: E501

        The upper circuit of symbol  # noqa: E501

        :return: The upper_circuit_limit of this MarketQuoteSymbol.  # noqa: E501
        :rtype: float
        """
        return self._upper_circuit_limit

    @upper_circuit_limit.setter
    def upper_circuit_limit(self, upper_circuit_limit):
        """Sets the upper_circuit_limit of this MarketQuoteSymbol.

        The upper circuit of symbol  # noqa: E501

        :param upper_circuit_limit: The upper_circuit_limit of this MarketQuoteSymbol.  # noqa: E501
        :type: float
        """

        self._upper_circuit_limit = upper_circuit_limit

    @property
    def last_trade_time(self):
        """Gets the last_trade_time of this MarketQuoteSymbol.  # noqa: E501

        Time in milliseconds at which last trade happened  # noqa: E501

        :return: The last_trade_time of this MarketQuoteSymbol.  # noqa: E501
        :rtype: str
        """
        return self._last_trade_time

    @last_trade_time.setter
    def last_trade_time(self, last_trade_time):
        """Sets the last_trade_time of this MarketQuoteSymbol.

        Time in milliseconds at which last trade happened  # noqa: E501

        :param last_trade_time: The last_trade_time of this MarketQuoteSymbol.  # noqa: E501
        :type: str
        """

        self._last_trade_time = last_trade_time

    @property
    def oi_day_high(self):
        """Gets the oi_day_high of this MarketQuoteSymbol.  # noqa: E501


        :return: The oi_day_high of this MarketQuoteSymbol.  # noqa: E501
        :rtype: float
        """
        return self._oi_day_high

    @oi_day_high.setter
    def oi_day_high(self, oi_day_high):
        """Sets the oi_day_high of this MarketQuoteSymbol.


        :param oi_day_high: The oi_day_high of this MarketQuoteSymbol.  # noqa: E501
        :type: float
        """

        self._oi_day_high = oi_day_high

    @property
    def oi_day_low(self):
        """Gets the oi_day_low of this MarketQuoteSymbol.  # noqa: E501


        :return: The oi_day_low of this MarketQuoteSymbol.  # noqa: E501
        :rtype: float
        """
        return self._oi_day_low

    @oi_day_low.setter
    def oi_day_low(self, oi_day_low):
        """Sets the oi_day_low of this MarketQuoteSymbol.


        :param oi_day_low: The oi_day_low of this MarketQuoteSymbol.  # noqa: E501
        :type: float
        """

        self._oi_day_low = oi_day_low

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(MarketQuoteSymbol, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MarketQuoteSymbol):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

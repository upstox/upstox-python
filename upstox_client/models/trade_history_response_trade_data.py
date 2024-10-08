# coding: utf-8

"""
    OpenAPI definition

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: v0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TradeHistoryResponseTradeData(object):
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
        'exchange': 'str',
        'segment': 'str',
        'option_type': 'str',
        'quantity': 'int',
        'amount': 'float',
        'trade_id': 'str',
        'trade_date': 'str',
        'transaction_type': 'str',
        'scrip_name': 'str',
        'strike_price': 'str',
        'expiry': 'str',
        'price': 'float',
        'isin': 'str',
        'symbol': 'str',
        'instrument_token': 'str'
    }

    attribute_map = {
        'exchange': 'exchange',
        'segment': 'segment',
        'option_type': 'option_type',
        'quantity': 'quantity',
        'amount': 'amount',
        'trade_id': 'trade_id',
        'trade_date': 'trade_date',
        'transaction_type': 'transaction_type',
        'scrip_name': 'scrip_name',
        'strike_price': 'strike_price',
        'expiry': 'expiry',
        'price': 'price',
        'isin': 'isin',
        'symbol': 'symbol',
        'instrument_token': 'instrument_token'
    }

    def __init__(self, exchange=None, segment=None, option_type=None, quantity=None, amount=None, trade_id=None, trade_date=None, transaction_type=None, scrip_name=None, strike_price=None, expiry=None, price=None, isin=None, symbol=None, instrument_token=None):  # noqa: E501
        """TradeHistoryResponseTradeData - a model defined in Swagger"""  # noqa: E501
        self._exchange = None
        self._segment = None
        self._option_type = None
        self._quantity = None
        self._amount = None
        self._trade_id = None
        self._trade_date = None
        self._transaction_type = None
        self._scrip_name = None
        self._strike_price = None
        self._expiry = None
        self._price = None
        self._isin = None
        self._symbol = None
        self._instrument_token = None
        self.discriminator = None
        if exchange is not None:
            self.exchange = exchange
        if segment is not None:
            self.segment = segment
        if option_type is not None:
            self.option_type = option_type
        if quantity is not None:
            self.quantity = quantity
        if amount is not None:
            self.amount = amount
        if trade_id is not None:
            self.trade_id = trade_id
        if trade_date is not None:
            self.trade_date = trade_date
        if transaction_type is not None:
            self.transaction_type = transaction_type
        if scrip_name is not None:
            self.scrip_name = scrip_name
        if strike_price is not None:
            self.strike_price = strike_price
        if expiry is not None:
            self.expiry = expiry
        if price is not None:
            self.price = price
        if isin is not None:
            self.isin = isin
        if symbol is not None:
            self.symbol = symbol
        if instrument_token is not None:
            self.instrument_token = instrument_token

    @property
    def exchange(self):
        """Gets the exchange of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The exchange of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: str
        """
        return self._exchange

    @exchange.setter
    def exchange(self, exchange):
        """Sets the exchange of this TradeHistoryResponseTradeData.


        :param exchange: The exchange of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: str
        """

        self._exchange = exchange

    @property
    def segment(self):
        """Gets the segment of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The segment of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: str
        """
        return self._segment

    @segment.setter
    def segment(self, segment):
        """Sets the segment of this TradeHistoryResponseTradeData.


        :param segment: The segment of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: str
        """

        self._segment = segment

    @property
    def option_type(self):
        """Gets the option_type of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The option_type of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: str
        """
        return self._option_type

    @option_type.setter
    def option_type(self, option_type):
        """Sets the option_type of this TradeHistoryResponseTradeData.


        :param option_type: The option_type of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: str
        """

        self._option_type = option_type

    @property
    def quantity(self):
        """Gets the quantity of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The quantity of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this TradeHistoryResponseTradeData.


        :param quantity: The quantity of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: int
        """

        self._quantity = quantity

    @property
    def amount(self):
        """Gets the amount of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The amount of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this TradeHistoryResponseTradeData.


        :param amount: The amount of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: float
        """

        self._amount = amount

    @property
    def trade_id(self):
        """Gets the trade_id of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The trade_id of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: str
        """
        return self._trade_id

    @trade_id.setter
    def trade_id(self, trade_id):
        """Sets the trade_id of this TradeHistoryResponseTradeData.


        :param trade_id: The trade_id of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: str
        """

        self._trade_id = trade_id

    @property
    def trade_date(self):
        """Gets the trade_date of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The trade_date of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: str
        """
        return self._trade_date

    @trade_date.setter
    def trade_date(self, trade_date):
        """Sets the trade_date of this TradeHistoryResponseTradeData.


        :param trade_date: The trade_date of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: str
        """

        self._trade_date = trade_date

    @property
    def transaction_type(self):
        """Gets the transaction_type of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The transaction_type of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: str
        """
        return self._transaction_type

    @transaction_type.setter
    def transaction_type(self, transaction_type):
        """Sets the transaction_type of this TradeHistoryResponseTradeData.


        :param transaction_type: The transaction_type of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: str
        """

        self._transaction_type = transaction_type

    @property
    def scrip_name(self):
        """Gets the scrip_name of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The scrip_name of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: str
        """
        return self._scrip_name

    @scrip_name.setter
    def scrip_name(self, scrip_name):
        """Sets the scrip_name of this TradeHistoryResponseTradeData.


        :param scrip_name: The scrip_name of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: str
        """

        self._scrip_name = scrip_name

    @property
    def strike_price(self):
        """Gets the strike_price of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The strike_price of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: str
        """
        return self._strike_price

    @strike_price.setter
    def strike_price(self, strike_price):
        """Sets the strike_price of this TradeHistoryResponseTradeData.


        :param strike_price: The strike_price of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: str
        """

        self._strike_price = strike_price

    @property
    def expiry(self):
        """Gets the expiry of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The expiry of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: str
        """
        return self._expiry

    @expiry.setter
    def expiry(self, expiry):
        """Sets the expiry of this TradeHistoryResponseTradeData.


        :param expiry: The expiry of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: str
        """

        self._expiry = expiry

    @property
    def price(self):
        """Gets the price of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The price of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: float
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this TradeHistoryResponseTradeData.


        :param price: The price of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: float
        """

        self._price = price

    @property
    def isin(self):
        """Gets the isin of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The isin of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: str
        """
        return self._isin

    @isin.setter
    def isin(self, isin):
        """Sets the isin of this TradeHistoryResponseTradeData.


        :param isin: The isin of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: str
        """

        self._isin = isin

    @property
    def symbol(self):
        """Gets the symbol of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The symbol of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: str
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        """Sets the symbol of this TradeHistoryResponseTradeData.


        :param symbol: The symbol of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: str
        """

        self._symbol = symbol

    @property
    def instrument_token(self):
        """Gets the instrument_token of this TradeHistoryResponseTradeData.  # noqa: E501


        :return: The instrument_token of this TradeHistoryResponseTradeData.  # noqa: E501
        :rtype: str
        """
        return self._instrument_token

    @instrument_token.setter
    def instrument_token(self, instrument_token):
        """Sets the instrument_token of this TradeHistoryResponseTradeData.


        :param instrument_token: The instrument_token of this TradeHistoryResponseTradeData.  # noqa: E501
        :type: str
        """

        self._instrument_token = instrument_token

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
        if issubclass(TradeHistoryResponseTradeData, dict):
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
        if not isinstance(other, TradeHistoryResponseTradeData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

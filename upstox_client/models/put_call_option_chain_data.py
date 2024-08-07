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

class PutCallOptionChainData(object):
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
        'instrument_key': 'str',
        'market_data': 'MarketData',
        'option_greeks': 'AnalyticsData'
    }

    attribute_map = {
        'instrument_key': 'instrument_key',
        'market_data': 'market_data',
        'option_greeks': 'option_greeks'
    }

    def __init__(self, instrument_key=None, market_data=None, option_greeks=None):  # noqa: E501
        """PutCallOptionChainData - a model defined in Swagger"""  # noqa: E501
        self._instrument_key = None
        self._market_data = None
        self._option_greeks = None
        self.discriminator = None
        if instrument_key is not None:
            self.instrument_key = instrument_key
        if market_data is not None:
            self.market_data = market_data
        if option_greeks is not None:
            self.option_greeks = option_greeks

    @property
    def instrument_key(self):
        """Gets the instrument_key of this PutCallOptionChainData.  # noqa: E501


        :return: The instrument_key of this PutCallOptionChainData.  # noqa: E501
        :rtype: str
        """
        return self._instrument_key

    @instrument_key.setter
    def instrument_key(self, instrument_key):
        """Sets the instrument_key of this PutCallOptionChainData.


        :param instrument_key: The instrument_key of this PutCallOptionChainData.  # noqa: E501
        :type: str
        """

        self._instrument_key = instrument_key

    @property
    def market_data(self):
        """Gets the market_data of this PutCallOptionChainData.  # noqa: E501


        :return: The market_data of this PutCallOptionChainData.  # noqa: E501
        :rtype: MarketData
        """
        return self._market_data

    @market_data.setter
    def market_data(self, market_data):
        """Sets the market_data of this PutCallOptionChainData.


        :param market_data: The market_data of this PutCallOptionChainData.  # noqa: E501
        :type: MarketData
        """

        self._market_data = market_data

    @property
    def option_greeks(self):
        """Gets the option_greeks of this PutCallOptionChainData.  # noqa: E501


        :return: The option_greeks of this PutCallOptionChainData.  # noqa: E501
        :rtype: AnalyticsData
        """
        return self._option_greeks

    @option_greeks.setter
    def option_greeks(self, option_greeks):
        """Sets the option_greeks of this PutCallOptionChainData.


        :param option_greeks: The option_greeks of this PutCallOptionChainData.  # noqa: E501
        :type: AnalyticsData
        """

        self._option_greeks = option_greeks

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
        if issubclass(PutCallOptionChainData, dict):
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
        if not isinstance(other, PutCallOptionChainData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

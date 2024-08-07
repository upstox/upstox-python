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

class HolidayData(object):
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
        '_date': 'datetime',
        'description': 'str',
        'holiday_type': 'str',
        'closed_exchanges': 'list[str]',
        'open_exchanges': 'list[ExchangeTimingData]'
    }

    attribute_map = {
        '_date': 'date',
        'description': 'description',
        'holiday_type': 'holiday_type',
        'closed_exchanges': 'closed_exchanges',
        'open_exchanges': 'open_exchanges'
    }

    def __init__(self, _date=None, description=None, holiday_type=None, closed_exchanges=None, open_exchanges=None):  # noqa: E501
        """HolidayData - a model defined in Swagger"""  # noqa: E501
        self.__date = None
        self._description = None
        self._holiday_type = None
        self._closed_exchanges = None
        self._open_exchanges = None
        self.discriminator = None
        if _date is not None:
            self._date = _date
        if description is not None:
            self.description = description
        if holiday_type is not None:
            self.holiday_type = holiday_type
        if closed_exchanges is not None:
            self.closed_exchanges = closed_exchanges
        if open_exchanges is not None:
            self.open_exchanges = open_exchanges

    @property
    def _date(self):
        """Gets the _date of this HolidayData.  # noqa: E501


        :return: The _date of this HolidayData.  # noqa: E501
        :rtype: datetime
        """
        return self.__date

    @_date.setter
    def _date(self, _date):
        """Sets the _date of this HolidayData.


        :param _date: The _date of this HolidayData.  # noqa: E501
        :type: datetime
        """

        self.__date = _date

    @property
    def description(self):
        """Gets the description of this HolidayData.  # noqa: E501


        :return: The description of this HolidayData.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this HolidayData.


        :param description: The description of this HolidayData.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def holiday_type(self):
        """Gets the holiday_type of this HolidayData.  # noqa: E501


        :return: The holiday_type of this HolidayData.  # noqa: E501
        :rtype: str
        """
        return self._holiday_type

    @holiday_type.setter
    def holiday_type(self, holiday_type):
        """Sets the holiday_type of this HolidayData.


        :param holiday_type: The holiday_type of this HolidayData.  # noqa: E501
        :type: str
        """
        allowed_values = ["ALL", "SETTLEMENT_HOLIDAY", "TRADING_HOLIDAY", "SPECIAL_TIMING"]  # noqa: E501
        if holiday_type not in allowed_values:
            raise ValueError(
                "Invalid value for `holiday_type` ({0}), must be one of {1}"  # noqa: E501
                .format(holiday_type, allowed_values)
            )

        self._holiday_type = holiday_type

    @property
    def closed_exchanges(self):
        """Gets the closed_exchanges of this HolidayData.  # noqa: E501


        :return: The closed_exchanges of this HolidayData.  # noqa: E501
        :rtype: list[str]
        """
        return self._closed_exchanges

    @closed_exchanges.setter
    def closed_exchanges(self, closed_exchanges):
        """Sets the closed_exchanges of this HolidayData.


        :param closed_exchanges: The closed_exchanges of this HolidayData.  # noqa: E501
        :type: list[str]
        """

        self._closed_exchanges = closed_exchanges

    @property
    def open_exchanges(self):
        """Gets the open_exchanges of this HolidayData.  # noqa: E501


        :return: The open_exchanges of this HolidayData.  # noqa: E501
        :rtype: list[ExchangeTimingData]
        """
        return self._open_exchanges

    @open_exchanges.setter
    def open_exchanges(self, open_exchanges):
        """Sets the open_exchanges of this HolidayData.


        :param open_exchanges: The open_exchanges of this HolidayData.  # noqa: E501
        :type: list[ExchangeTimingData]
        """

        self._open_exchanges = open_exchanges

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
        if issubclass(HolidayData, dict):
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
        if not isinstance(other, HolidayData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

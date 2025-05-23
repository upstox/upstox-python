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

class BrokerageTaxes(object):
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
        'gst': 'float',
        'stt': 'float',
        'stamp_duty': 'float'
    }

    attribute_map = {
        'gst': 'gst',
        'stt': 'stt',
        'stamp_duty': 'stamp_duty'
    }

    def __init__(self, gst=None, stt=None, stamp_duty=None):  # noqa: E501
        """BrokerageTaxes - a model defined in Swagger"""  # noqa: E501
        self._gst = None
        self._stt = None
        self._stamp_duty = None
        self.discriminator = None
        if gst is not None:
            self.gst = gst
        if stt is not None:
            self.stt = stt
        if stamp_duty is not None:
            self.stamp_duty = stamp_duty

    @property
    def gst(self):
        """Gets the gst of this BrokerageTaxes.  # noqa: E501

        GST charges  # noqa: E501

        :return: The gst of this BrokerageTaxes.  # noqa: E501
        :rtype: float
        """
        return self._gst

    @gst.setter
    def gst(self, gst):
        """Sets the gst of this BrokerageTaxes.

        GST charges  # noqa: E501

        :param gst: The gst of this BrokerageTaxes.  # noqa: E501
        :type: float
        """

        self._gst = gst

    @property
    def stt(self):
        """Gets the stt of this BrokerageTaxes.  # noqa: E501

        STT charges  # noqa: E501

        :return: The stt of this BrokerageTaxes.  # noqa: E501
        :rtype: float
        """
        return self._stt

    @stt.setter
    def stt(self, stt):
        """Sets the stt of this BrokerageTaxes.

        STT charges  # noqa: E501

        :param stt: The stt of this BrokerageTaxes.  # noqa: E501
        :type: float
        """

        self._stt = stt

    @property
    def stamp_duty(self):
        """Gets the stamp_duty of this BrokerageTaxes.  # noqa: E501

        Stamp duty charges  # noqa: E501

        :return: The stamp_duty of this BrokerageTaxes.  # noqa: E501
        :rtype: float
        """
        return self._stamp_duty

    @stamp_duty.setter
    def stamp_duty(self, stamp_duty):
        """Sets the stamp_duty of this BrokerageTaxes.

        Stamp duty charges  # noqa: E501

        :param stamp_duty: The stamp_duty of this BrokerageTaxes.  # noqa: E501
        :type: float
        """

        self._stamp_duty = stamp_duty

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
        if issubclass(BrokerageTaxes, dict):
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
        if not isinstance(other, BrokerageTaxes):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

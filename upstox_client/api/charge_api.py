# coding: utf-8

"""
    Upstox Developer API

    Build your App on the Upstox platform  ![Banner](https://api.upstox.com/api-docs/images/banner.jpg \"banner\")  # Introduction  Upstox API is a set of rest APIs that provide data required to build a complete investment and trading platform. Execute orders in real time, manage user portfolio, stream live market data (using Websocket), and more, with the easy to understand API collection.  All requests are over HTTPS and the requests are sent with the content-type ‘application/json’. Developers have the option of choosing the response type as JSON or CSV for a few API calls.  To be able to use these APIs you need to create an App in the Developer Console and generate your **apiKey** and **apiSecret**. You can use a redirect URL which will be called after the login flow.  If you are a **trader**, you can directly create apps from Upstox mobile app or the desktop platform itself from **Apps** sections inside the **Account** Tab. Head over to <a href=\"http://account.upstox.com/developer/apps\" target=\"_blank\">account.upstox.com/developer/apps</a>.</br> If you are a **business** looking to integrate Upstox APIs, reach out to us and we will get a custom app created for you in no time.  It is highly recommended that you do not embed the **apiSecret** in your frontend app. Create a remote backend which does the handshake on behalf of the frontend app. Marking the apiSecret in the frontend app will make your app vulnerable to threats and potential issues.   # noqa: E501

    OpenAPI spec version: v2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from upstox_client.api_client import ApiClient


class ChargeApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_brokerage(self, instrument_token, quantity, product, transaction_type, price, api_version, **kwargs):  # noqa: E501
        """Brokerage details  # noqa: E501

        Compute Brokerage Charges  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_brokerage(instrument_token, quantity, product, transaction_type, price, api_version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str instrument_token: Key of the instrument (required)
        :param int quantity: Quantity with which the order is to be placed (required)
        :param str product: Product with which the order is to be placed (required)
        :param str transaction_type: Indicates whether its a BUY or SELL order (required)
        :param float price: Price with which the order is to be placed (required)
        :param str api_version: API Version Header (required)
        :return: GetBrokerageResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_brokerage_with_http_info(instrument_token, quantity, product, transaction_type, price, api_version, **kwargs)  # noqa: E501
        else:
            (data) = self.get_brokerage_with_http_info(instrument_token, quantity, product, transaction_type, price, api_version, **kwargs)  # noqa: E501
            return data

    def get_brokerage_with_http_info(self, instrument_token, quantity, product, transaction_type, price, api_version, **kwargs):  # noqa: E501
        """Brokerage details  # noqa: E501

        Compute Brokerage Charges  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_brokerage_with_http_info(instrument_token, quantity, product, transaction_type, price, api_version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str instrument_token: Key of the instrument (required)
        :param int quantity: Quantity with which the order is to be placed (required)
        :param str product: Product with which the order is to be placed (required)
        :param str transaction_type: Indicates whether its a BUY or SELL order (required)
        :param float price: Price with which the order is to be placed (required)
        :param str api_version: API Version Header (required)
        :return: GetBrokerageResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['instrument_token', 'quantity', 'product', 'transaction_type', 'price', 'api_version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_brokerage" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'instrument_token' is set
        if ('instrument_token' not in params or
                params['instrument_token'] is None):
            raise ValueError("Missing the required parameter `instrument_token` when calling `get_brokerage`")  # noqa: E501
        # verify the required parameter 'quantity' is set
        if ('quantity' not in params or
                params['quantity'] is None):
            raise ValueError("Missing the required parameter `quantity` when calling `get_brokerage`")  # noqa: E501
        # verify the required parameter 'product' is set
        if ('product' not in params or
                params['product'] is None):
            raise ValueError("Missing the required parameter `product` when calling `get_brokerage`")  # noqa: E501
        # verify the required parameter 'transaction_type' is set
        if ('transaction_type' not in params or
                params['transaction_type'] is None):
            raise ValueError("Missing the required parameter `transaction_type` when calling `get_brokerage`")  # noqa: E501
        # verify the required parameter 'price' is set
        if ('price' not in params or
                params['price'] is None):
            raise ValueError("Missing the required parameter `price` when calling `get_brokerage`")  # noqa: E501
        # verify the required parameter 'api_version' is set
        if ('api_version' not in params or
                params['api_version'] is None):
            raise ValueError("Missing the required parameter `api_version` when calling `get_brokerage`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'instrument_token' in params:
            query_params.append(('instrument_token', params['instrument_token']))  # noqa: E501
        if 'quantity' in params:
            query_params.append(('quantity', params['quantity']))  # noqa: E501
        if 'product' in params:
            query_params.append(('product', params['product']))  # noqa: E501
        if 'transaction_type' in params:
            query_params.append(('transaction_type', params['transaction_type']))  # noqa: E501
        if 'price' in params:
            query_params.append(('price', params['price']))  # noqa: E501

        header_params = {}
        if 'api_version' in params:
            header_params['Api-Version'] = params['api_version']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', '*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAUTH2']  # noqa: E501

        return self.api_client.call_api(
            '/v2/charges/brokerage', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetBrokerageResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_margin(self, body, **kwargs):  # noqa: E501
        """Calculate Margin  # noqa: E501

        Compute Margin  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_margin(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MarginRequest body: (required)
        :return: PostMarginResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.post_margin_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.post_margin_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def post_margin_with_http_info(self, body, **kwargs):  # noqa: E501
        """Calculate Margin  # noqa: E501

        Compute Margin  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_margin_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MarginRequest body: (required)
        :return: PostMarginResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_margin" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `post_margin`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', '*/*'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAUTH2']  # noqa: E501

        return self.api_client.call_api(
            '/v2/charges/margin', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PostMarginResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

# coding: utf-8

"""
    OpenAPI definition

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: v0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from upstox_client.api_client import ApiClient


class MarketQuoteV3Api(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_ltp(self, **kwargs):  # noqa: E501
        """Market quotes and instruments - LTP quotes.  # noqa: E501

        This API provides the functionality to retrieve the LTP quotes for one or more instruments.This API returns the LTPs of up to 500 instruments in one go.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_ltp(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str instrument_key: Comma separated list of instrument keys
        :return: GetMarketQuoteLastTradedPriceResponseV3
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_ltp_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_ltp_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_ltp_with_http_info(self, **kwargs):  # noqa: E501
        """Market quotes and instruments - LTP quotes.  # noqa: E501

        This API provides the functionality to retrieve the LTP quotes for one or more instruments.This API returns the LTPs of up to 500 instruments in one go.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_ltp_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str instrument_key: Comma separated list of instrument keys
        :return: GetMarketQuoteLastTradedPriceResponseV3
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['instrument_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_ltp" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'instrument_key' in params:
            query_params.append(('instrument_key', params['instrument_key']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', '*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAUTH2']  # noqa: E501

        return self.api_client.call_api(
            '/v3/market-quote/ltp', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetMarketQuoteLastTradedPriceResponseV3',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_market_quote_ohlc(self, interval, **kwargs):  # noqa: E501
        """Market quotes and instruments - OHLC quotes  # noqa: E501

        This API provides the functionality to retrieve the OHLC quotes for one or more instruments.This API returns the OHLC snapshots of up to 500 instruments in one go.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_market_quote_ohlc(interval, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str interval: Interval to get ohlc data (required)
        :param str instrument_key: Comma separated list of instrument keys
        :return: GetMarketQuoteOHLCResponseV3
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_market_quote_ohlc_with_http_info(interval, **kwargs)  # noqa: E501
        else:
            (data) = self.get_market_quote_ohlc_with_http_info(interval, **kwargs)  # noqa: E501
            return data

    def get_market_quote_ohlc_with_http_info(self, interval, **kwargs):  # noqa: E501
        """Market quotes and instruments - OHLC quotes  # noqa: E501

        This API provides the functionality to retrieve the OHLC quotes for one or more instruments.This API returns the OHLC snapshots of up to 500 instruments in one go.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_market_quote_ohlc_with_http_info(interval, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str interval: Interval to get ohlc data (required)
        :param str instrument_key: Comma separated list of instrument keys
        :return: GetMarketQuoteOHLCResponseV3
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['interval', 'instrument_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_market_quote_ohlc" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'interval' is set
        if ('interval' not in params or
                params['interval'] is None):
            raise ValueError("Missing the required parameter `interval` when calling `get_market_quote_ohlc`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'instrument_key' in params:
            query_params.append(('instrument_key', params['instrument_key']))  # noqa: E501
        if 'interval' in params:
            query_params.append(('interval', params['interval']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', '*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAUTH2']  # noqa: E501

        return self.api_client.call_api(
            '/v3/market-quote/ohlc', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetMarketQuoteOHLCResponseV3',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_market_quote_option_greek(self, **kwargs):  # noqa: E501
        """Market quotes and instruments - Option Greek  # noqa: E501

        This API provides the functionality to retrieve the Option Greek data for one or more instruments.This API returns the Option Greek data of up to 500 instruments in one go.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_market_quote_option_greek(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str instrument_key: Comma separated list of instrument keys
        :return: GetMarketQuoteOptionGreekResponseV3
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_market_quote_option_greek_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_market_quote_option_greek_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_market_quote_option_greek_with_http_info(self, **kwargs):  # noqa: E501
        """Market quotes and instruments - Option Greek  # noqa: E501

        This API provides the functionality to retrieve the Option Greek data for one or more instruments.This API returns the Option Greek data of up to 500 instruments in one go.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_market_quote_option_greek_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str instrument_key: Comma separated list of instrument keys
        :return: GetMarketQuoteOptionGreekResponseV3
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['instrument_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_market_quote_option_greek" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'instrument_key' in params:
            query_params.append(('instrument_key', params['instrument_key']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', '*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAUTH2']  # noqa: E501

        return self.api_client.call_api(
            '/v3/market-quote/option-greek', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetMarketQuoteOptionGreekResponseV3',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

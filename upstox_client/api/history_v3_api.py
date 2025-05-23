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


class HistoryV3Api(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_historical_candle_data(self, instrument_key, unit, interval, to_date, **kwargs):  # noqa: E501
        """Historical candle data  # noqa: E501

        Get OHLC values for all instruments for the present trading day with expanded interval options.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_historical_candle_data(instrument_key, unit, interval, to_date, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str instrument_key: (required)
        :param str unit: (required)
        :param int interval: (required)
        :param str to_date: (required)
        :return: GetHistoricalCandleResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_historical_candle_data_with_http_info(instrument_key, unit, interval, to_date, **kwargs)  # noqa: E501
        else:
            (data) = self.get_historical_candle_data_with_http_info(instrument_key, unit, interval, to_date, **kwargs)  # noqa: E501
            return data

    def get_historical_candle_data_with_http_info(self, instrument_key, unit, interval, to_date, **kwargs):  # noqa: E501
        """Historical candle data  # noqa: E501

        Get OHLC values for all instruments for the present trading day with expanded interval options.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_historical_candle_data_with_http_info(instrument_key, unit, interval, to_date, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str instrument_key: (required)
        :param str unit: (required)
        :param int interval: (required)
        :param str to_date: (required)
        :return: GetHistoricalCandleResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['instrument_key', 'unit', 'interval', 'to_date']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_historical_candle_data" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'instrument_key' is set
        if ('instrument_key' not in params or
                params['instrument_key'] is None):
            raise ValueError("Missing the required parameter `instrument_key` when calling `get_historical_candle_data`")  # noqa: E501
        # verify the required parameter 'unit' is set
        if ('unit' not in params or
                params['unit'] is None):
            raise ValueError("Missing the required parameter `unit` when calling `get_historical_candle_data`")  # noqa: E501
        # verify the required parameter 'interval' is set
        if ('interval' not in params or
                params['interval'] is None):
            raise ValueError("Missing the required parameter `interval` when calling `get_historical_candle_data`")  # noqa: E501
        # verify the required parameter 'to_date' is set
        if ('to_date' not in params or
                params['to_date'] is None):
            raise ValueError("Missing the required parameter `to_date` when calling `get_historical_candle_data`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'instrument_key' in params:
            path_params['instrumentKey'] = params['instrument_key']  # noqa: E501
        if 'unit' in params:
            path_params['unit'] = params['unit']  # noqa: E501
        if 'interval' in params:
            path_params['interval'] = params['interval']  # noqa: E501
        if 'to_date' in params:
            path_params['to_date'] = params['to_date']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', '*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/v3/historical-candle/{instrumentKey}/{unit}/{interval}/{to_date}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetHistoricalCandleResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_historical_candle_data1(self, instrument_key, unit, interval, to_date, from_date, **kwargs):  # noqa: E501
        """Historical candle data  # noqa: E501

        Get OHLC values for all instruments for the present trading day with expanded interval options  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_historical_candle_data1(instrument_key, unit, interval, to_date, from_date, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str instrument_key: (required)
        :param str unit: (required)
        :param int interval: (required)
        :param str to_date: (required)
        :param str from_date: (required)
        :return: GetHistoricalCandleResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_historical_candle_data1_with_http_info(instrument_key, unit, interval, to_date, from_date, **kwargs)  # noqa: E501
        else:
            (data) = self.get_historical_candle_data1_with_http_info(instrument_key, unit, interval, to_date, from_date, **kwargs)  # noqa: E501
            return data

    def get_historical_candle_data1_with_http_info(self, instrument_key, unit, interval, to_date, from_date, **kwargs):  # noqa: E501
        """Historical candle data  # noqa: E501

        Get OHLC values for all instruments for the present trading day with expanded interval options  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_historical_candle_data1_with_http_info(instrument_key, unit, interval, to_date, from_date, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str instrument_key: (required)
        :param str unit: (required)
        :param int interval: (required)
        :param str to_date: (required)
        :param str from_date: (required)
        :return: GetHistoricalCandleResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['instrument_key', 'unit', 'interval', 'to_date', 'from_date']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_historical_candle_data1" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'instrument_key' is set
        if ('instrument_key' not in params or
                params['instrument_key'] is None):
            raise ValueError("Missing the required parameter `instrument_key` when calling `get_historical_candle_data1`")  # noqa: E501
        # verify the required parameter 'unit' is set
        if ('unit' not in params or
                params['unit'] is None):
            raise ValueError("Missing the required parameter `unit` when calling `get_historical_candle_data1`")  # noqa: E501
        # verify the required parameter 'interval' is set
        if ('interval' not in params or
                params['interval'] is None):
            raise ValueError("Missing the required parameter `interval` when calling `get_historical_candle_data1`")  # noqa: E501
        # verify the required parameter 'to_date' is set
        if ('to_date' not in params or
                params['to_date'] is None):
            raise ValueError("Missing the required parameter `to_date` when calling `get_historical_candle_data1`")  # noqa: E501
        # verify the required parameter 'from_date' is set
        if ('from_date' not in params or
                params['from_date'] is None):
            raise ValueError("Missing the required parameter `from_date` when calling `get_historical_candle_data1`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'instrument_key' in params:
            path_params['instrumentKey'] = params['instrument_key']  # noqa: E501
        if 'unit' in params:
            path_params['unit'] = params['unit']  # noqa: E501
        if 'interval' in params:
            path_params['interval'] = params['interval']  # noqa: E501
        if 'to_date' in params:
            path_params['to_date'] = params['to_date']  # noqa: E501
        if 'from_date' in params:
            path_params['from_date'] = params['from_date']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', '*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/v3/historical-candle/{instrumentKey}/{unit}/{interval}/{to_date}/{from_date}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetHistoricalCandleResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_intra_day_candle_data(self, instrument_key, unit, interval, **kwargs):  # noqa: E501
        """Intra day candle data  # noqa: E501

        Get OHLC values for all instruments for the present trading day  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_intra_day_candle_data(instrument_key, unit, interval, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str instrument_key: (required)
        :param str unit: (required)
        :param int interval: (required)
        :return: GetIntraDayCandleResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_intra_day_candle_data_with_http_info(instrument_key, unit, interval, **kwargs)  # noqa: E501
        else:
            (data) = self.get_intra_day_candle_data_with_http_info(instrument_key, unit, interval, **kwargs)  # noqa: E501
            return data

    def get_intra_day_candle_data_with_http_info(self, instrument_key, unit, interval, **kwargs):  # noqa: E501
        """Intra day candle data  # noqa: E501

        Get OHLC values for all instruments for the present trading day  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_intra_day_candle_data_with_http_info(instrument_key, unit, interval, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str instrument_key: (required)
        :param str unit: (required)
        :param int interval: (required)
        :return: GetIntraDayCandleResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['instrument_key', 'unit', 'interval']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_intra_day_candle_data" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'instrument_key' is set
        if ('instrument_key' not in params or
                params['instrument_key'] is None):
            raise ValueError("Missing the required parameter `instrument_key` when calling `get_intra_day_candle_data`")  # noqa: E501
        # verify the required parameter 'unit' is set
        if ('unit' not in params or
                params['unit'] is None):
            raise ValueError("Missing the required parameter `unit` when calling `get_intra_day_candle_data`")  # noqa: E501
        # verify the required parameter 'interval' is set
        if ('interval' not in params or
                params['interval'] is None):
            raise ValueError("Missing the required parameter `interval` when calling `get_intra_day_candle_data`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'instrument_key' in params:
            path_params['instrumentKey'] = params['instrument_key']  # noqa: E501
        if 'unit' in params:
            path_params['unit'] = params['unit']  # noqa: E501
        if 'interval' in params:
            path_params['interval'] = params['interval']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', '*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/v3/historical-candle/intraday/{instrumentKey}/{unit}/{interval}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetIntraDayCandleResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

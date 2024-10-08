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


class PostTradeApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_trades_by_date_range(self, start_date, end_date, page_number, page_size, **kwargs):  # noqa: E501
        """Get historical trades  # noqa: E501

        This API retrieves the trade history for a specified time interval.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_trades_by_date_range(start_date, end_date, page_number, page_size, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str start_date: Date from which trade history needs to be fetched. Date in YYYY-mm-dd format (required)
        :param str end_date: Date till which history needs needs to be fetched. Date in YYYY-mm-dd format (required)
        :param int page_number: Page number for which you want to fetch trade history  (required)
        :param int page_size: How many records you want for a page  (required)
        :param str segment: Segment for which data is requested can be from the following options EQ - Equity,   FO - Futures and Options,   COM  - Commodity,   CD - Currency Derivatives MF - Mutual Funds
        :return: TradeHistoryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_trades_by_date_range_with_http_info(start_date, end_date, page_number, page_size, **kwargs)  # noqa: E501
        else:
            (data) = self.get_trades_by_date_range_with_http_info(start_date, end_date, page_number, page_size, **kwargs)  # noqa: E501
            return data

    def get_trades_by_date_range_with_http_info(self, start_date, end_date, page_number, page_size, **kwargs):  # noqa: E501
        """Get historical trades  # noqa: E501

        This API retrieves the trade history for a specified time interval.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_trades_by_date_range_with_http_info(start_date, end_date, page_number, page_size, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str start_date: Date from which trade history needs to be fetched. Date in YYYY-mm-dd format (required)
        :param str end_date: Date till which history needs needs to be fetched. Date in YYYY-mm-dd format (required)
        :param int page_number: Page number for which you want to fetch trade history  (required)
        :param int page_size: How many records you want for a page  (required)
        :param str segment: Segment for which data is requested can be from the following options EQ - Equity,   FO - Futures and Options,   COM  - Commodity,   CD - Currency Derivatives MF - Mutual Funds
        :return: TradeHistoryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['start_date', 'end_date', 'page_number', 'page_size', 'segment']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_trades_by_date_range" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'start_date' is set
        if ('start_date' not in params or
                params['start_date'] is None):
            raise ValueError("Missing the required parameter `start_date` when calling `get_trades_by_date_range`")  # noqa: E501
        # verify the required parameter 'end_date' is set
        if ('end_date' not in params or
                params['end_date'] is None):
            raise ValueError("Missing the required parameter `end_date` when calling `get_trades_by_date_range`")  # noqa: E501
        # verify the required parameter 'page_number' is set
        if ('page_number' not in params or
                params['page_number'] is None):
            raise ValueError("Missing the required parameter `page_number` when calling `get_trades_by_date_range`")  # noqa: E501
        # verify the required parameter 'page_size' is set
        if ('page_size' not in params or
                params['page_size'] is None):
            raise ValueError("Missing the required parameter `page_size` when calling `get_trades_by_date_range`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'segment' in params:
            query_params.append(('segment', params['segment']))  # noqa: E501
        if 'start_date' in params:
            query_params.append(('start_date', params['start_date']))  # noqa: E501
        if 'end_date' in params:
            query_params.append(('end_date', params['end_date']))  # noqa: E501
        if 'page_number' in params:
            query_params.append(('page_number', params['page_number']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('page_size', params['page_size']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAUTH2']  # noqa: E501

        return self.api_client.call_api(
            '/v2/charges/historical-trades', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TradeHistoryResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

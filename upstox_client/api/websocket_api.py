# coding: utf-8

"""
    Upstox Developer API

    Build your App on the Upstox platform  ![Banner](https://api-v2.upstox.com/api-docs/images/banner.jpg \"banner\")  # Introduction  Upstox API is a set of rest APIs that provide data required to build a complete investment and trading platform. Execute orders in real time, manage user portfolio, stream live market data (using Websocket), and more, with the easy to understand API collection.  All requests are over HTTPS and the requests are sent with the content-type ‘application/json’. Developers have the option of choosing the response type as JSON or CSV for a few API calls.  To be able to use these APIs you need to create an App in the Developer Console and generate your **apiKey** and **apiSecret**. You can use a redirect URL which will be called after the login flow.  If you are a **trader**, you can directly create apps from Upstox mobile app or the desktop platform itself from **Apps** sections inside the **Account** Tab. Head over to <a href=\"http://account.upstox.com/developer/apps\" target=\"_blank\">account.upstox.com/developer/apps</a>.</br> If you are a **business** looking to integrate Upstox APIs, reach out to us and we will get a custom app created for you in no time.  It is highly recommended that you do not embed the **apiSecret** in your frontend app. Create a remote backend which does the handshake on behalf of the frontend app. Marking the apiSecret in the frontend app will make your app vulnerable to threats and potential issues.   # noqa: E501

    OpenAPI spec version: v2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from upstox_client.api_client import ApiClient


class WebsocketApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.order_update = True
        self.holding_update = False
        self.position_update = False

    def get_market_data_feed(self, api_version, **kwargs):  # noqa: E501
        """Market Data Feed  # noqa: E501

         This API redirects the client to the respective socket endpoint to receive Market updates.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_market_data_feed(api_version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_version: API Version Header (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_market_data_feed_with_http_info(api_version, **kwargs)  # noqa: E501
        else:
            (data) = self.get_market_data_feed_with_http_info(api_version, **kwargs)  # noqa: E501
            return data

    def get_market_data_feed_with_http_info(self, api_version, **kwargs):  # noqa: E501
        """Market Data Feed  # noqa: E501

         This API redirects the client to the respective socket endpoint to receive Market updates.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_market_data_feed_with_http_info(api_version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_version: API Version Header (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_market_data_feed" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_version' is set
        if ('api_version' not in params or
                params['api_version'] is None):
            raise ValueError("Missing the required parameter `api_version` when calling `get_market_data_feed`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        resource_path = '/v3/feed/market-data-feed'
        header_params = {}
        if 'api_version' in params:
            header_params['Api-Version'] = params['api_version'] # noqa: E501
            if params['api_version'] == "2.0":
                resource_path = '/v2/feed/market-data-feed'


        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAUTH2']  # noqa: E501

        return self.api_client.call_api(
            resource_path, 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_market_data_feed_authorize(self, api_version, **kwargs):  # noqa: E501
        """Market Data Feed Authorize  # noqa: E501

        This API provides the functionality to retrieve the socket endpoint URI for Market updates.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_market_data_feed_authorize(api_version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_version: API Version Header (required)
        :return: WebsocketAuthRedirectResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_market_data_feed_authorize_with_http_info(api_version, **kwargs)  # noqa: E501
        else:
            (data) = self.get_market_data_feed_authorize_with_http_info(api_version, **kwargs)  # noqa: E501
            return data

    def get_market_data_feed_authorize_with_http_info(self, api_version, **kwargs):  # noqa: E501
        """Market Data Feed Authorize  # noqa: E501

        This API provides the functionality to retrieve the socket endpoint URI for Market updates.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_market_data_feed_authorize_with_http_info(api_version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_version: API Version Header (required)
        :return: WebsocketAuthRedirectResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_market_data_feed_authorize" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_version' is set
        if ('api_version' not in params or
                params['api_version'] is None):
            raise ValueError("Missing the required parameter `api_version` when calling `get_market_data_feed_authorize`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        resource_path = '/v3/feed/market-data-feed/authorize'
        header_params = {}
        if 'api_version' in params:
            header_params['Api-Version'] = params['api_version'] # noqa: E501
            if params['api_version'] == "2.0":
                resource_path = '/v2/feed/market-data-feed/authorize'

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAUTH2']  # noqa: E501

        return self.api_client.call_api(resource_path, 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WebsocketAuthRedirectResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_portfolio_stream_feed(self, api_version, **kwargs):  # noqa: E501
        """Portfolio Stream Feed  # noqa: E501

        This API redirects the client to the respective socket endpoint to receive Portfolio updates.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_portfolio_stream_feed(api_version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_version: API Version Header (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_portfolio_stream_feed_with_http_info(api_version, **kwargs)  # noqa: E501
        else:
            (data) = self.get_portfolio_stream_feed_with_http_info(api_version, **kwargs)  # noqa: E501
            return data

    def get_portfolio_stream_feed_with_http_info(self, api_version, **kwargs):  # noqa: E501
        """Portfolio Stream Feed  # noqa: E501

        This API redirects the client to the respective socket endpoint to receive Portfolio updates.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_portfolio_stream_feed_with_http_info(api_version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_version: API Version Header (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_portfolio_stream_feed" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_version' is set
        if ('api_version' not in params or
                params['api_version'] is None):
            raise ValueError("Missing the required parameter `api_version` when calling `get_portfolio_stream_feed`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}
        if 'api_version' in params:
            header_params['Api-Version'] = params['api_version']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAUTH2']  # noqa: E501

        return self.api_client.call_api(
            '/v2/feed/portfolio-stream-feed', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_portfolio_stream_feed_authorize(self, api_version,  order_update=True, position_update=False,holding_update=False,**kwargs):  # noqa: E501
        """Portfolio Stream Feed Authorize  # noqa: E501

         This API provides the functionality to retrieve the socket endpoint URI for Portfolio updates.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_portfolio_stream_feed_authorize(api_version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_version: API Version Header (required)
        :return: WebsocketAuthRedirectResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        self.position_update = position_update
        self.holding_update = holding_update
        self.order_update = order_update
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_portfolio_stream_feed_authorize_with_http_info(api_version, **kwargs)  # noqa: E501
        else:
            (data) = self.get_portfolio_stream_feed_authorize_with_http_info(api_version, **kwargs)  # noqa: E501
            return data

    def get_portfolio_stream_feed_authorize_with_http_info(self, api_version, **kwargs):  # noqa: E501
        """Portfolio Stream Feed Authorize  # noqa: E501

         This API provides the functionality to retrieve the socket endpoint URI for Portfolio updates.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_portfolio_stream_feed_authorize_with_http_info(api_version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_version: API Version Header (required)
        :return: WebsocketAuthRedirectResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_portfolio_stream_feed_authorize" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_version' is set
        if ('api_version' not in params or
                params['api_version'] is None):
            raise ValueError("Missing the required parameter `api_version` when calling `get_portfolio_stream_feed_authorize`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}
        if 'api_version' in params:
            header_params['Api-Version'] = params['api_version']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAUTH2']  # noqa: E501

        return self.api_client.call_api(
            '/v2/feed/portfolio-stream-feed/authorize' + self.get_websocket_parameters(), 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WebsocketAuthRedirectResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_websocket_parameters(self):
        params = ""
        update_types = []
        if self.order_update:
            update_types.append("order")
        if self.holding_update:
            update_types.append("holding")
        if self.position_update:
            update_types.append("position")

        if update_types:
            params += "?update_types=" + "%2C".join(update_types)
        return params

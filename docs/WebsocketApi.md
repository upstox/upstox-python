# swagger_client.WebsocketApi

All URIs are relative to *https://api-v2.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_market_data_feed**](WebsocketApi.md#get_market_data_feed) | **GET** /feed/market-data-feed | Market Data Feed
[**get_market_data_feed_authorize**](WebsocketApi.md#get_market_data_feed_authorize) | **GET** /feed/market-data-feed/authorize | Market Data Feed Authorize
[**get_portfolio_stream_feed**](WebsocketApi.md#get_portfolio_stream_feed) | **GET** /feed/portfolio-stream-feed | Portfolio Stream Feed
[**get_portfolio_stream_feed_authorize**](WebsocketApi.md#get_portfolio_stream_feed_authorize) | **GET** /feed/portfolio-stream-feed/authorize | Portfolio Stream Feed Authorize

# **get_market_data_feed**
> get_market_data_feed(api_version)

Market Data Feed

 This API redirects the client to the respective socket endpoint to receive Market updates.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = swagger_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.WebsocketApi(swagger_client.ApiClient(configuration))
api_version = 'api_version_example' # str | API Version Header

try:
    # Market Data Feed
    api_instance.get_market_data_feed(api_version)
except ApiException as e:
    print("Exception when calling WebsocketApi->get_market_data_feed: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_version** | **str**| API Version Header | 

### Return type

void (empty response body)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_market_data_feed_authorize**
> WebsocketAuthRedirectResponse get_market_data_feed_authorize(api_version)

Market Data Feed Authorize

This API provides the functionality to retrieve the socket endpoint URI for Market updates.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = swagger_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.WebsocketApi(swagger_client.ApiClient(configuration))
api_version = 'api_version_example' # str | API Version Header

try:
    # Market Data Feed Authorize
    api_response = api_instance.get_market_data_feed_authorize(api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WebsocketApi->get_market_data_feed_authorize: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_version** | **str**| API Version Header | 

### Return type

[**WebsocketAuthRedirectResponse**](WebsocketAuthRedirectResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_portfolio_stream_feed**
> get_portfolio_stream_feed(api_version)

Portfolio Stream Feed

This API redirects the client to the respective socket endpoint to receive Portfolio updates.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = swagger_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.WebsocketApi(swagger_client.ApiClient(configuration))
api_version = 'api_version_example' # str | API Version Header

try:
    # Portfolio Stream Feed
    api_instance.get_portfolio_stream_feed(api_version)
except ApiException as e:
    print("Exception when calling WebsocketApi->get_portfolio_stream_feed: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_version** | **str**| API Version Header | 

### Return type

void (empty response body)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_portfolio_stream_feed_authorize**
> WebsocketAuthRedirectResponse get_portfolio_stream_feed_authorize(api_version)

Portfolio Stream Feed Authorize

 This API provides the functionality to retrieve the socket endpoint URI for Portfolio updates.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = swagger_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.WebsocketApi(swagger_client.ApiClient(configuration))
api_version = 'api_version_example' # str | API Version Header

try:
    # Portfolio Stream Feed Authorize
    api_response = api_instance.get_portfolio_stream_feed_authorize(api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WebsocketApi->get_portfolio_stream_feed_authorize: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_version** | **str**| API Version Header | 

### Return type

[**WebsocketAuthRedirectResponse**](WebsocketAuthRedirectResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


# upstox_client.OrderApi

All URIs are relative to *https://api.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cancel_multi_order**](OrderApi.md#cancel_multi_order) | **DELETE** /v2/order/multi/cancel | Cancel multi order
[**cancel_order1**](OrderApi.md#cancel_order1) | **DELETE** /v2/order/cancel | Cancel order
[**exit_positions**](OrderApi.md#exit_positions) | **POST** /v2/order/positions/exit | Exit all positions
[**get_order_book**](OrderApi.md#get_order_book) | **GET** /v2/order/retrieve-all | Get order book
[**get_order_details**](OrderApi.md#get_order_details) | **GET** /v2/order/history | Get order history
[**get_order_status**](OrderApi.md#get_order_status) | **GET** /v2/order/details | Get order details
[**get_trade_history**](OrderApi.md#get_trade_history) | **GET** /v2/order/trades/get-trades-for-day | Get trades
[**get_trades_by_order**](OrderApi.md#get_trades_by_order) | **GET** /v2/order/trades | Get trades for order
[**modify_order1**](OrderApi.md#modify_order1) | **PUT** /v2/order/modify | Modify order
[**place_multi_order**](OrderApi.md#place_multi_order) | **POST** /v2/order/multi/place | Place multi order
[**place_order1**](OrderApi.md#place_order1) | **POST** /v2/order/place | Place order

# **cancel_multi_order**
> CancelOrExitMultiOrderResponse cancel_multi_order(tag=tag, segment=segment)

Cancel multi order

API to cancel all the open or pending orders which can be applied to both AMO and regular orders.

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = upstox_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
tag = 'tag_example' # str | The tag associated with the orders for which the orders must be cancelled (optional)
segment = 'segment_example' # str | The segment for which the orders must be cancelled (optional)

try:
    # Cancel multi order
    api_response = api_instance.cancel_multi_order(tag=tag, segment=segment)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->cancel_multi_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tag** | **str**| The tag associated with the orders for which the orders must be cancelled | [optional] 
 **segment** | **str**| The segment for which the orders must be cancelled | [optional] 

### Return type

[**CancelOrExitMultiOrderResponse**](CancelOrExitMultiOrderResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cancel_order1**
> CancelOrderResponse cancel_order1(order_id)

Cancel order

Cancel order API can be used for two purposes: Cancelling an open order which could be an AMO or a normal order It is also used to EXIT a CO or OCO(bracket order)

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = upstox_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
order_id = 'order_id_example' # str | The order ID for which the order must be cancelled
api_version = 'api_version_example' # str | API Version Header

try:
    # Cancel order
    api_response = api_instance.cancel_order(order_id, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->cancel_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**| The order ID for which the order must be cancelled | 
 **api_version** | **str**| API Version Header | 

### Return type

[**CancelOrderResponse**](CancelOrderResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **exit_positions**
> CancelOrExitMultiOrderResponse exit_positions(tag=tag, segment=segment)

Exit all positions

This API provides the functionality to exit all the positions 

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = upstox_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
tag = 'tag_example' # str | The tag associated with the positions for which the positions must be exit (optional)
segment = 'segment_example' # str | The segment for which the positions must be exit (optional)

try:
    # Exit all positions
    api_response = api_instance.exit_positions(tag=tag, segment=segment)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->exit_positions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tag** | **str**| The tag associated with the positions for which the positions must be exit | [optional] 
 **segment** | **str**| The segment for which the positions must be exit | [optional] 

### Return type

[**CancelOrExitMultiOrderResponse**](CancelOrExitMultiOrderResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_order_book**
> GetOrderBookResponse get_order_book(api_version)

Get order book

This API provides the list of orders placed by the user. The orders placed by the user is transient for a day and is cleared by the end of the trading session. This API returns all states of the orders, namely, open, pending, and filled ones.

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = upstox_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
api_version = 'api_version_example' # str | API Version Header

try:
    # Get order book
    api_response = api_instance.get_order_book(api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_order_book: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_version** | **str**| API Version Header | 

### Return type

[**GetOrderBookResponse**](GetOrderBookResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_order_details**
> GetOrderResponse get_order_details(api_version, order_id=order_id, tag=tag)

Get order details

This API provides the details of the particular order the user has placed. The orders placed by the user is transient for a day and are cleared by the end of the trading session. This API returns all states of the orders, namely, open, pending, and filled ones.  The order history can be requested either using order_id or tag.  If both the options are passed, the history of the order which precisely matches both the order_id and tag will be returned in the response.  If only the tag is passed, the history of all the associated orders which matches the tag will be shared in the response.

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = upstox_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
api_version = 'api_version_example' # str | API Version Header
order_id = 'order_id_example' # str | The order reference ID for which the order history is required (optional)
tag = 'tag_example' # str | The unique tag of the order for which the order history is being requested (optional)

try:
    # Get order details
    api_response = api_instance.get_order_details(api_version, order_id=order_id, tag=tag)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_order_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_version** | **str**| API Version Header | 
 **order_id** | **str**| The order reference ID for which the order history is required | [optional] 
 **tag** | **str**| The unique tag of the order for which the order history is being requested | [optional] 

### Return type

[**GetOrderResponse**](GetOrderResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_order_status**
> GetOrderDetailsResponse get_order_status(order_id=order_id)

Get order details

This API provides the recent detail of the particular order the user has placed. The orders placed by the user is transient for a day and are cleared by the end of the trading session.\\n\\nThe order details can be requested using order_id.  

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = upstox_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
order_id = 'order_id_example' # str | The order reference ID for which the order details is required (optional)

try:
    # Get order details
    api_response = api_instance.get_order_status(order_id=order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_order_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**| The order reference ID for which the order details is required | [optional] 

### Return type

[**GetOrderDetailsResponse**](GetOrderDetailsResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trade_history**
> GetTradeResponse get_trade_history(api_version)

Get trades

Retrieve the trades executed for the day

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = upstox_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
api_version = 'api_version_example' # str | API Version Header

try:
    # Get trades
    api_response = api_instance.get_trade_history(api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_trade_history: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_version** | **str**| API Version Header | 

### Return type

[**GetTradeResponse**](GetTradeResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trades_by_order**
> GetTradeResponse get_trades_by_order(order_id, api_version)

Get trades for order

Retrieve the trades executed for an order

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = upstox_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
order_id = 'order_id_example' # str | The order ID for which the order to get order trades
api_version = 'api_version_example' # str | API Version Header

try:
    # Get trades for order
    api_response = api_instance.get_trades_by_order(order_id, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_trades_by_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**| The order ID for which the order to get order trades | 
 **api_version** | **str**| API Version Header | 

### Return type

[**GetTradeResponse**](GetTradeResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_order**
> ModifyOrderResponse modify_order(body, api_version)

Modify order

This API allows you to modify an order. For modification orderId is mandatory. With orderId you need to send the optional parameter which needs to be modified. In case the optional parameters aren't sent, the default will be considered from the original order

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = upstox_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.ModifyOrderRequest() # ModifyOrderRequest | 
api_version = 'api_version_example' # str | API Version Header

try:
    # Modify order
    api_response = api_instance.modify_order(body, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->modify_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModifyOrderRequest**](ModifyOrderRequest.md)|  | 
 **api_version** | **str**| API Version Header | 

### Return type

[**ModifyOrderResponse**](ModifyOrderResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **place_multi_order**
> MultiOrderResponse place_multi_order(body)

Place multi order

This API allows you to place multiple orders to the exchange via Upstox.

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = upstox_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = [upstox_client.MultiOrderRequest()] # list[MultiOrderRequest] | 

try:
    # Place multi order
    api_response = api_instance.place_multi_order(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_multi_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[MultiOrderRequest]**](MultiOrderRequest.md)|  | 

### Return type

[**MultiOrderResponse**](MultiOrderResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **place_order1**
> PlaceOrderResponse place_order1(body)

Place order

This API allows you to place an order to the exchange via Upstox.

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = upstox_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest() # PlaceOrderRequest | 
api_version = 'api_version_example' # str | API Version Header

try:
    # Place order
    api_response = api_instance.place_order(body, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PlaceOrderRequest**](PlaceOrderRequest.md)|  | 
 **api_version** | **str**| API Version Header | 

### Return type

[**PlaceOrderResponse**](PlaceOrderResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


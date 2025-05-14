# upstox_client.OrderApiV3

All URIs are relative to *https://api.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cancel_order**](OrderApiV3.md#cancel_order) | **DELETE** /v3/order/cancel | 
[**modify_order**](OrderApiV3.md#modify_order) | **PUT** /v3/order/modify | 
[**place_order**](OrderApiV3.md#place_order) | **POST** /v3/order/place | 

# **cancel_gtt_order**
> GttTriggerOrderResponse cancel_gtt_order(body)

Cancel GTT order

This API allows you to cancel GTT orders.

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
api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))
body = upstox_client.GttCancelOrderRequest() # GttCancelOrderRequest | 

try:
    # Cancel GTT order
    api_response = api_instance.cancel_gtt_order(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApiV3->cancel_gtt_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**GttCancelOrderRequest**](GttCancelOrderRequest.md)|  | 

### Return type

[**GttTriggerOrderResponse**](GttTriggerOrderResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cancel_order**
> CancelOrderV3Response cancel_order(order_id)



### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = upstox_client.OrderApiV3()
order_id = 'order_id_example' # str | 

try:
    api_response = api_instance.cancel_order(order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApiV3->cancel_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**|  |

### Return type

[**CancelOrderV3Response**](CancelOrderV3Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_gtt_order_details**
> GetGttOrderResponse get_gtt_order_details(gtt_order_id=gtt_order_id)

Get GTT order details

GTT_ORDER_DESCRIPTION

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
api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))
gtt_order_id = 'gtt_order_id_example' # str | Unique identifier of the GTT order for which the order history is required (optional)

try:
    # Get GTT order details
    api_response = api_instance.get_gtt_order_details(gtt_order_id=gtt_order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApiV3->get_gtt_order_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **gtt_order_id** | **str**| Unique identifier of the GTT order for which the order history is required | [optional] 

### Return type

[**GetGttOrderResponse**](GetGttOrderResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_gtt_order**
> GttTriggerOrderResponse modify_gtt_order(body)

Modify GTT order

This API allows you to modify GTT orders.

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
api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))
body = upstox_client.GttModifyOrderRequest() # GttModifyOrderRequest | 

try:
    # Modify GTT order
    api_response = api_instance.modify_gtt_order(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApiV3->modify_gtt_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**GttModifyOrderRequest**](GttModifyOrderRequest.md)|  | 

### Return type

[**GttTriggerOrderResponse**](GttTriggerOrderResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_order**
> ModifyOrderV3Response modify_order(body)



### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = upstox_client.OrderApiV3()
body = upstox_client.ModifyOrderRequest() # ModifyOrderRequest | 

try:
    api_response = api_instance.modify_order(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApiV3->modify_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModifyOrderRequest**](ModifyOrderRequest.md)|  |

### Return type

[**ModifyOrderV3Response**](ModifyOrderV3Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **place_gtt_order**
> GttTriggerOrderResponse place_gtt_order(body)

Place GTT order

This API allows you to place GTT orders.

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
api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))
body = upstox_client.GttPlaceOrderRequest() # GttPlaceOrderRequest | 

try:
    # Place GTT order
    api_response = api_instance.place_gtt_order(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApiV3->place_gtt_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**GttPlaceOrderRequest**](GttPlaceOrderRequest.md)|  | 

### Return type

[**GttTriggerOrderResponse**](GttTriggerOrderResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **place_order**
> PlaceOrderV3Response place_order(body)



### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = upstox_client.OrderApiV3()
body = upstox_client.PlaceOrderV3Request() # PlaceOrderV3Request | 

try:
    api_response = api_instance.place_order(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApiV3->place_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PlaceOrderV3Request**](PlaceOrderV3Request.md)|  |

### Return type

[**PlaceOrderV3Response**](PlaceOrderV3Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


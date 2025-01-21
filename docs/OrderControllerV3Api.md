# upstox_client.OrderApiV3

All URIs are relative to *https://api-v2.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cancel_order**](OrderApiV3.md#cancel_order) | **DELETE** /v3/order/cancel | 
[**modify_order**](OrderApiV3.md#modify_order) | **PUT** /v3/order/modify | 
[**place_order**](OrderApiV3.md#place_order) | **POST** /v3/order/place | 

# **cancel_order**
> CancelOrderV3Response cancel_order(order_id, origin=origin)



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
origin = 'origin_example' # str |  (optional)

try:
    api_response = api_instance.cancel_order(order_id, origin=origin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApiV3->cancel_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**|  | 
 **origin** | **str**|  | [optional] 

### Return type

[**CancelOrderV3Response**](CancelOrderV3Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_order**
> ModifyOrderV3Response modify_order(body, origin=origin)



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
origin = 'origin_example' # str |  (optional)

try:
    api_response = api_instance.modify_order(body, origin=origin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApiV3->modify_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModifyOrderRequest**](ModifyOrderRequest.md)|  | 
 **origin** | **str**|  | [optional] 

### Return type

[**ModifyOrderV3Response**](ModifyOrderV3Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **place_order**
> PlaceOrderV3Response place_order(body, origin=origin)



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
origin = 'origin_example' # str |  (optional)

try:
    api_response = api_instance.place_order(body, origin=origin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApiV3->place_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PlaceOrderV3Request**](PlaceOrderV3Request.md)|  | 
 **origin** | **str**|  | [optional] 

### Return type

[**PlaceOrderV3Response**](PlaceOrderV3Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


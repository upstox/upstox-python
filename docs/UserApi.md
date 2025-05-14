# upstox_client.UserApi

All URIs are relative to *https://api.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_profile**](UserApi.md#get_profile) | **GET** /user/profile | Get profile
[**get_user_fund_margin**](UserApi.md#get_user_fund_margin) | **GET** /user/get-funds-and-margin | Get User Fund And Margin

# **get_profile**
> GetProfileResponse get_profile(api_version)

Get profile

This API allows to fetch the complete information of the user who is logged in including the products, order types and exchanges enabled for the user

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
api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))
api_version = 'api_version_example' # str | API Version Header

try:
    # Get profile
    api_response = api_instance.get_profile(api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_profile: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_version** | **str**| API Version Header | 

### Return type

[**GetProfileResponse**](GetProfileResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_fund_margin**
> GetUserFundMarginResponse get_user_fund_margin(api_version, segment=segment)

Get User Fund And Margin

Shows the balance of the user in equity and commodity market.

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
api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))
api_version = 'api_version_example' # str | API Version Header
segment = 'segment_example' # str |  (optional)

try:
    # Get User Fund And Margin
    api_response = api_instance.get_user_fund_margin(api_version, segment=segment)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_user_fund_margin: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_version** | **str**| API Version Header | 
 **segment** | **str**|  | [optional] 

### Return type

[**GetUserFundMarginResponse**](GetUserFundMarginResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


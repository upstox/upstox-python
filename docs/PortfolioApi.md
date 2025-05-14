# upstox_client.PortfolioApi

All URIs are relative to *https://api.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**convert_positions**](PortfolioApi.md#convert_positions) | **PUT** /portfolio/convert-position | Convert Positions
[**get_holdings**](PortfolioApi.md#get_holdings) | **GET** /portfolio/long-term-holdings | Get Holdings
[**get_positions**](PortfolioApi.md#get_positions) | **GET** /portfolio/short-term-positions | Get Positions

# **convert_positions**
> ConvertPositionResponse convert_positions(body, api_version)

Convert Positions

Convert the margin product of an open position

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
api_instance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))
body = upstox_client.ConvertPositionRequest() # ConvertPositionRequest | 
api_version = 'api_version_example' # str | API Version Header

try:
    # Convert Positions
    api_response = api_instance.convert_positions(body, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortfolioApi->convert_positions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConvertPositionRequest**](ConvertPositionRequest.md)|  | 
 **api_version** | **str**| API Version Header | 

### Return type

[**ConvertPositionResponse**](ConvertPositionResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_holdings**
> GetHoldingsResponse get_holdings(api_version)

Get Holdings

Fetches the holdings which the user has bought/sold in previous trading sessions.

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
api_instance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))
api_version = 'api_version_example' # str | API Version Header

try:
    # Get Holdings
    api_response = api_instance.get_holdings(api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortfolioApi->get_holdings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_version** | **str**| API Version Header | 

### Return type

[**GetHoldingsResponse**](GetHoldingsResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_positions**
> GetPositionResponse get_positions(api_version)

Get Positions

Fetches the current positions for the user for the current day.

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
api_instance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))
api_version = 'api_version_example' # str | API Version Header

try:
    # Get Positions
    api_response = api_instance.get_positions(api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortfolioApi->get_positions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_version** | **str**| API Version Header | 

### Return type

[**GetPositionResponse**](GetPositionResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


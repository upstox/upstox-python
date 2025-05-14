# swagger_client.MarketHolidaysAndTimingsApi

All URIs are relative to *https://api.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_exchange_timings**](MarketHolidaysAndTimingsApi.md#get_exchange_timings) | **GET** /v2/market/timings/{date} | Get Exchange Timings on particular date
[**get_holiday**](MarketHolidaysAndTimingsApi.md#get_holiday) | **GET** /v2/market/holidays/{date} | Get Holiday on particular date
[**get_holidays**](MarketHolidaysAndTimingsApi.md#get_holidays) | **GET** /v2/market/holidays | Get Holiday list of current year
[**get_market_status**](MarketHolidaysAndTimingsApi.md#get_market_status) | **GET** /v2/market/status/{exchange} | Get Market status for particular exchange

# **get_exchange_timings**
> GetExchangeTimingResponse get_exchange_timings(_date)

Get Exchange Timings on particular date

This API provides the functionality to retrieve the exchange timings on particular date

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MarketHolidaysAndTimingsApi()
_date = '_date_example' # str | 

try:
    # Get Exchange Timings on particular date
    api_response = api_instance.get_exchange_timings(_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi->get_exchange_timings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_date** | **str**|  | 

### Return type

[**GetExchangeTimingResponse**](GetExchangeTimingResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_holiday**
> GetHolidayResponse get_holiday(_date)

Get Holiday on particular date

This API provides the functionality to retrieve the holiday on particular date

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MarketHolidaysAndTimingsApi()
_date = '_date_example' # str | 

try:
    # Get Holiday on particular date
    api_response = api_instance.get_holiday(_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi->get_holiday: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_date** | **str**|  | 

### Return type

[**GetHolidayResponse**](GetHolidayResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_holidays**
> GetHolidayResponse get_holidays()

Get Holiday list of current year

This API provides the functionality to retrieve the holiday list of current year

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MarketHolidaysAndTimingsApi()

try:
    # Get Holiday list of current year
    api_response = api_instance.get_holidays()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi->get_holidays: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**GetHolidayResponse**](GetHolidayResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_market_status**
> GetMarketStatusResponse get_market_status(exchange)

Get Market status for particular exchange

This API provides the functionality to retrieve the market status for particular exchange

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
api_instance = swagger_client.MarketHolidaysAndTimingsApi(swagger_client.ApiClient(configuration))
exchange = 'exchange_example' # str | 

try:
    # Get Market status for particular exchange
    api_response = api_instance.get_market_status(exchange)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi->get_market_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exchange** | **str**|  | 

### Return type

[**GetMarketStatusResponse**](GetMarketStatusResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


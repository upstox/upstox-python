# upstox_client.HistoryApi

All URIs are relative to *https://api-v2.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_historical_candle_data**](HistoryApi.md#get_historical_candle_data) | **GET** /historical-candle/{instrumentKey}/{interval}/{to_date} | Historical candle data
[**get_historical_candle_data1**](HistoryApi.md#get_historical_candle_data1) | **GET** /historical-candle/{instrumentKey}/{interval}/{to_date}/{from_date} | Historical candle data
[**get_intra_day_candle_data**](HistoryApi.md#get_intra_day_candle_data) | **GET** /historical-candle/intraday/{instrumentKey}/{interval} | Intra day candle data

# **get_historical_candle_data**
> GetHistoricalCandleResponse get_historical_candle_data(instrument_key, interval, to_date, api_version)

Historical candle data

Get OHLC values for all instruments across various timeframes. Historical data can be fetched for the following durations. 1minute: last 1 month candles till endDate 30minute: last 1 year candles till endDate day: last 1 year candles till endDate week: last 10 year candles till endDate month: last 10 year candles till endDate

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = upstox_client.HistoryApi()
instrument_key = 'instrument_key_example' # str | 
interval = 'interval_example' # str | 
to_date = 'to_date_example' # str | 
api_version = 'api_version_example' # str | API Version Header

try:
    # Historical candle data
    api_response = api_instance.get_historical_candle_data(instrument_key, interval, to_date, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instrument_key** | **str**|  | 
 **interval** | **str**|  | 
 **to_date** | **str**|  | 
 **api_version** | **str**| API Version Header | 

### Return type

[**GetHistoricalCandleResponse**](GetHistoricalCandleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_historical_candle_data1**
> GetHistoricalCandleResponse get_historical_candle_data1(instrument_key, interval, to_date, from_date, api_version)

Historical candle data

Get OHLC values for all instruments across various timeframes. Historical data can be fetched for the following durations. 1minute: last 1 month candles till endDate 30minute: last 1 year candles till endDate day: last 1 year candles till endDate week: last 10 year candles till endDate month: last 10 year candles till endDate

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = upstox_client.HistoryApi()
instrument_key = 'instrument_key_example' # str | 
interval = 'interval_example' # str | 
to_date = 'to_date_example' # str | 
from_date = 'from_date_example' # str | 
api_version = 'api_version_example' # str | API Version Header

try:
    # Historical candle data
    api_response = api_instance.get_historical_candle_data1(instrument_key, interval, to_date, from_date, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instrument_key** | **str**|  | 
 **interval** | **str**|  | 
 **to_date** | **str**|  | 
 **from_date** | **str**|  | 
 **api_version** | **str**| API Version Header | 

### Return type

[**GetHistoricalCandleResponse**](GetHistoricalCandleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_intra_day_candle_data**
> GetIntraDayCandleResponse get_intra_day_candle_data(instrument_key, interval, api_version)

Intra day candle data

Get OHLC values for all instruments for the present trading day

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = upstox_client.HistoryApi()
instrument_key = 'instrument_key_example' # str | 
interval = 'interval_example' # str | 
api_version = 'api_version_example' # str | API Version Header

try:
    # Intra day candle data
    api_response = api_instance.get_intra_day_candle_data(instrument_key, interval, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_intra_day_candle_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instrument_key** | **str**|  | 
 **interval** | **str**|  | 
 **api_version** | **str**| API Version Header | 

### Return type

[**GetIntraDayCandleResponse**](GetIntraDayCandleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


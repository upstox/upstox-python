# upstox_client.HistoryV3Api

All URIs are relative to *https://api-v2.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_historical_candle_data**](HistoryV3Api.md#get_historical_candle_data) | **GET** /v3/historical-candle/{instrumentKey}/{unit}/{interval}/{to_date} | Historical candle data
[**get_historical_candle_data1**](HistoryV3Api.md#get_historical_candle_data1) | **GET** /v3/historical-candle/{instrumentKey}/{unit}/{interval}/{to_date}/{from_date} | Historical candle data
[**get_intra_day_candle_data**](HistoryV3Api.md#get_intra_day_candle_data) | **GET** /v3/historical-candle/intraday/{instrumentKey}/{unit}/{interval} | Intra day candle data

# **get_historical_candle_data**
> GetHistoricalCandleResponse get_historical_candle_data(instrument_key, unit, interval, to_date)

Historical candle data

Get OHLC values for all instruments for the present trading day with expanded interval options.

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = upstox_client.HistoryV3Api()
instrument_key = 'instrument_key_example' # str | 
unit = 'unit_example' # str | 
interval = 56 # int | 
to_date = 'to_date_example' # str | 

try:
    # Historical candle data
    api_response = api_instance.get_historical_candle_data(instrument_key, unit, interval, to_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HistoryV3Api->get_historical_candle_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instrument_key** | **str**|  | 
 **unit** | **str**|  | 
 **interval** | **int**|  | 
 **to_date** | **str**|  | 

### Return type

[**GetHistoricalCandleResponse**](GetHistoricalCandleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_historical_candle_data1**
> GetHistoricalCandleResponse get_historical_candle_data1(instrument_key, unit, interval, to_date, from_date)

Historical candle data

Get OHLC values for all instruments for the present trading day with expanded interval options

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = upstox_client.HistoryV3Api()
instrument_key = 'instrument_key_example' # str | 
unit = 'unit_example' # str | 
interval = 56 # int | 
to_date = 'to_date_example' # str | 
from_date = 'from_date_example' # str | 

try:
    # Historical candle data
    api_response = api_instance.get_historical_candle_data1(instrument_key, unit, interval, to_date, from_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HistoryV3Api->get_historical_candle_data1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instrument_key** | **str**|  | 
 **unit** | **str**|  | 
 **interval** | **int**|  | 
 **to_date** | **str**|  | 
 **from_date** | **str**|  | 

### Return type

[**GetHistoricalCandleResponse**](GetHistoricalCandleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_intra_day_candle_data**
> GetIntraDayCandleResponse get_intra_day_candle_data(instrument_key, unit, interval)

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
api_instance = upstox_client.HistoryV3Api()
instrument_key = 'instrument_key_example' # str | 
unit = 'unit_example' # str | 
interval = 56 # int | 

try:
    # Intra day candle data
    api_response = api_instance.get_intra_day_candle_data(instrument_key, unit, interval)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HistoryV3Api->get_intra_day_candle_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instrument_key** | **str**|  | 
 **unit** | **str**|  | 
 **interval** | **int**|  | 

### Return type

[**GetIntraDayCandleResponse**](GetIntraDayCandleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


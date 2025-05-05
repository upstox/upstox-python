# upstox_client.ExpiredInstrumentApi

All URIs are relative to *https://api-v2.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_expired_future_contracts**](ExpiredInstrumentApi.md#get_expired_future_contracts) | **GET** /v2/expired-instruments/future/contract | Expired instruments - Get future contracts
[**get_expired_historical_candle_data**](ExpiredInstrumentApi.md#get_expired_historical_candle_data) | **GET** /v2/expired-instruments/historical-candle/{expired_instrument_key}/{interval}/{to_date}/{from_date} | Expired Historical candle data
[**get_expired_option_contracts**](ExpiredInstrumentApi.md#get_expired_option_contracts) | **GET** /v2/expired-instruments/option/contract | Get expired option contracts
[**get_expiries**](ExpiredInstrumentApi.md#get_expiries) | **GET** /v2/expired-instruments/expiries | Expired instruments - Get expiries

# **get_expired_future_contracts**
> GetExpiredFuturesContractResponse get_expired_future_contracts(instrument_key, expiry_date)

Expired instruments - Get future contracts

This API provides the functionality to retrieve expired future contracts for a given instrument key and expiry date.

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
api_instance = upstox_client.ExpiredInstrumentApi(upstox_client.ApiClient(configuration))
instrument_key = 'instrument_key_example' # str | Instrument Key of asset
expiry_date = 'expiry_date_example' # str | Expiry date of the instrument

try:
    # Expired instruments - Get future contracts
    api_response = api_instance.get_expired_future_contracts(instrument_key, expiry_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExpiredInstrumentApi->get_expired_future_contracts: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instrument_key** | **str**| Instrument Key of asset | 
 **expiry_date** | **str**| Expiry date of the instrument | 

### Return type

[**GetExpiredFuturesContractResponse**](GetExpiredFuturesContractResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_expired_historical_candle_data**
> GetHistoricalCandleResponse get_expired_historical_candle_data(expired_instrument_key, interval, to_date, from_date)

Expired Historical candle data

Get Expired OHLC values for all instruments across various timeframes. Expired Historical data can be fetched for the following durations. 1minute: last 1 month candles till endDate 30minute: last 1 year candles till endDate day: last 1 year candles till endDate week: last 10 year candles till endDate month: last 10 year candles till endDate

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
api_instance = upstox_client.ExpiredInstrumentApi(upstox_client.ApiClient(configuration))
expired_instrument_key = 'expired_instrument_key_example' # str | Expired Instrument Key of asset
interval = 'interval_example' # str | Interval to get expired ohlc data
to_date = 'to_date_example' # str | to date
from_date = 'from_date_example' # str | from date

try:
    # Expired Historical candle data
    api_response = api_instance.get_expired_historical_candle_data(expired_instrument_key, interval, to_date, from_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExpiredInstrumentApi->get_expired_historical_candle_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expired_instrument_key** | **str**| Expired Instrument Key of asset | 
 **interval** | **str**| Interval to get expired ohlc data | 
 **to_date** | **str**| to date | 
 **from_date** | **str**| from date | 

### Return type

[**GetHistoricalCandleResponse**](GetHistoricalCandleResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_expired_option_contracts**
> GetOptionContractResponse get_expired_option_contracts(instrument_key, expiry_date)

Get expired option contracts

This API provides the functionality to retrieve the expired option contracts

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
api_instance = upstox_client.ExpiredInstrumentApi(upstox_client.ApiClient(configuration))
instrument_key = 'instrument_key_example' # str | Instrument key for an underlying symbol
expiry_date = 'expiry_date_example' # str | Expiry date in format: YYYY-mm-dd

try:
    # Get expired option contracts
    api_response = api_instance.get_expired_option_contracts(instrument_key, expiry_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExpiredInstrumentApi->get_expired_option_contracts: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instrument_key** | **str**| Instrument key for an underlying symbol | 
 **expiry_date** | **str**| Expiry date in format: YYYY-mm-dd | 

### Return type

[**GetOptionContractResponse**](GetOptionContractResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_expiries**
> GetExpiriesResponse get_expiries(instrument_key)

Expired instruments - Get expiries

This API provides the functionality to retrieve expiry dates for a given instrument key.

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
api_instance = upstox_client.ExpiredInstrumentApi(upstox_client.ApiClient(configuration))
instrument_key = 'instrument_key_example' # str | Instrument Key of asset

try:
    # Expired instruments - Get expiries
    api_response = api_instance.get_expiries(instrument_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExpiredInstrumentApi->get_expiries: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instrument_key** | **str**| Instrument Key of asset | 

### Return type

[**GetExpiriesResponse**](GetExpiriesResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


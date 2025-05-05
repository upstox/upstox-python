# upstox_client.MarketQuoteV3Api

All URIs are relative to *https://api-v2.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_ltp**](MarketQuoteV3Api.md#get_ltp) | **GET** /v3/market-quote/ltp | Market quotes and instruments - LTP quotes.
[**get_market_quote_ohlc**](MarketQuoteV3Api.md#get_market_quote_ohlc) | **GET** /v3/market-quote/ohlc | Market quotes and instruments - OHLC quotes
[**get_market_quote_option_greek**](MarketQuoteV3Api.md#get_market_quote_option_greek) | **GET** /v3/market-quote/option-greek | Market quotes and instruments - Option Greek

# **get_ltp**
> GetMarketQuoteLastTradedPriceResponseV3 get_ltp(instrument_key=instrument_key)

Market quotes and instruments - LTP quotes.

This API provides the functionality to retrieve the LTP quotes for one or more instruments.This API returns the LTPs of up to 500 instruments in one go.

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
api_instance = upstox_client.MarketQuoteV3Api(upstox_client.ApiClient(configuration))
instrument_key = 'instrument_key_example' # str | Comma separated list of instrument keys (optional)

try:
    # Market quotes and instruments - LTP quotes.
    api_response = api_instance.get_ltp(instrument_key=instrument_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_ltp: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instrument_key** | **str**| Comma separated list of instrument keys | [optional] 

### Return type

[**GetMarketQuoteLastTradedPriceResponseV3**](GetMarketQuoteLastTradedPriceResponseV3.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_market_quote_ohlc**
> GetMarketQuoteOHLCResponseV3 get_market_quote_ohlc(interval, instrument_key=instrument_key)

Market quotes and instruments - OHLC quotes

This API provides the functionality to retrieve the OHLC quotes for one or more instruments.This API returns the OHLC snapshots of up to 500 instruments in one go.

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
api_instance = upstox_client.MarketQuoteV3Api(upstox_client.ApiClient(configuration))
interval = 'interval_example' # str | Interval to get ohlc data
instrument_key = 'instrument_key_example' # str | Comma separated list of instrument keys (optional)

try:
    # Market quotes and instruments - OHLC quotes
    api_response = api_instance.get_market_quote_ohlc(interval, instrument_key=instrument_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_market_quote_ohlc: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **interval** | **str**| Interval to get ohlc data | 
 **instrument_key** | **str**| Comma separated list of instrument keys | [optional] 

### Return type

[**GetMarketQuoteOHLCResponseV3**](GetMarketQuoteOHLCResponseV3.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_market_quote_option_greek**
> GetMarketQuoteOptionGreekResponseV3 get_market_quote_option_greek(instrument_key=instrument_key)

Market quotes and instruments - Option Greek

This API provides the functionality to retrieve the Option Greek data for one or more instruments.This API returns the Option Greek data of up to 500 instruments in one go.

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
api_instance = upstox_client.MarketQuoteV3Api(upstox_client.ApiClient(configuration))
instrument_key = 'instrument_key_example' # str | Comma separated list of instrument keys (optional)

try:
    # Market quotes and instruments - Option Greek
    api_response = api_instance.get_market_quote_option_greek(instrument_key=instrument_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_market_quote_option_greek: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instrument_key** | **str**| Comma separated list of instrument keys | [optional] 

### Return type

[**GetMarketQuoteOptionGreekResponseV3**](GetMarketQuoteOptionGreekResponseV3.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


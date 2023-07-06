# swagger_client.MarketQuoteApi

All URIs are relative to *https://api-v2.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_full_market_quote**](MarketQuoteApi.md#get_full_market_quote) | **GET** /market-quote/quotes | Market quotes and instruments - Full market quotes
[**get_market_quote_ohlc**](MarketQuoteApi.md#get_market_quote_ohlc) | **GET** /market-quote/ohlc | Market quotes and instruments - OHLC quotes
[**ltp**](MarketQuoteApi.md#ltp) | **GET** /market-quote/ltp | Market quotes and instruments - LTP quotes.

# **get_full_market_quote**
> GetFullMarketQuoteResponse get_full_market_quote(symbol, api_version)

Market quotes and instruments - Full market quotes

This API provides the functionality to retrieve the full market quotes for one or more instruments.This API returns the complete market data snapshot of up to 500 instruments in one go.

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
api_instance = swagger_client.MarketQuoteApi(swagger_client.ApiClient(configuration))
symbol = 'symbol_example' # str | Comma separated list of symbols
api_version = 'api_version_example' # str | API Version Header

try:
    # Market quotes and instruments - Full market quotes
    api_response = api_instance.get_full_market_quote(symbol, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **symbol** | **str**| Comma separated list of symbols | 
 **api_version** | **str**| API Version Header | 

### Return type

[**GetFullMarketQuoteResponse**](GetFullMarketQuoteResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_market_quote_ohlc**
> GetMarketQuoteOHLCResponse get_market_quote_ohlc(symbol, interval, api_version)

Market quotes and instruments - OHLC quotes

This API provides the functionality to retrieve the OHLC quotes for one or more instruments.This API returns the OHLC snapshots of up to 1000 instruments in one go.

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
api_instance = swagger_client.MarketQuoteApi(swagger_client.ApiClient(configuration))
symbol = 'symbol_example' # str | Comma separated list of symbols
interval = 'interval_example' # str | Interval to get ohlc data
api_version = 'api_version_example' # str | API Version Header

try:
    # Market quotes and instruments - OHLC quotes
    api_response = api_instance.get_market_quote_ohlc(symbol, interval, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MarketQuoteApi->get_market_quote_ohlc: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **symbol** | **str**| Comma separated list of symbols | 
 **interval** | **str**| Interval to get ohlc data | 
 **api_version** | **str**| API Version Header | 

### Return type

[**GetMarketQuoteOHLCResponse**](GetMarketQuoteOHLCResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ltp**
> GetMarketQuoteLastTradedPriceResponse ltp(symbol, api_version)

Market quotes and instruments - LTP quotes.

This API provides the functionality to retrieve the LTP quotes for one or more instruments.This API returns the LTPs of up to 1000 instruments in one go.

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
api_instance = swagger_client.MarketQuoteApi(swagger_client.ApiClient(configuration))
symbol = 'symbol_example' # str | Comma separated list of symbols
api_version = 'api_version_example' # str | API Version Header

try:
    # Market quotes and instruments - LTP quotes.
    api_response = api_instance.ltp(symbol, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MarketQuoteApi->ltp: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **symbol** | **str**| Comma separated list of symbols | 
 **api_version** | **str**| API Version Header | 

### Return type

[**GetMarketQuoteLastTradedPriceResponse**](GetMarketQuoteLastTradedPriceResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


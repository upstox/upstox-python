# swagger_client.PostTradeApi

All URIs are relative to *https://api.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_trades_by_date_range**](PostTradeApi.md#get_trades_by_date_range) | **GET** /v2/charges/historical-trades | Get historical trades

# **get_trades_by_date_range**
> TradeHistoryResponse get_trades_by_date_range(start_date, end_date, page_number, page_size, segment=segment)

Get historical trades

This API retrieves the trade history for a specified time interval.

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
api_instance = swagger_client.PostTradeApi(swagger_client.ApiClient(configuration))
start_date = 'start_date_example' # str | Date from which trade history needs to be fetched. Date in YYYY-mm-dd format
end_date = 'end_date_example' # str | Date till which history needs needs to be fetched. Date in YYYY-mm-dd format
page_number = 56 # int | Page number for which you want to fetch trade history 
page_size = 56 # int | How many records you want for a page 
segment = '' # str | Segment for which data is requested can be from the following options EQ - Equity,   FO - Futures and Options,   COM  - Commodity,   CD - Currency Derivatives MF - Mutual Funds (optional)

try:
    # Get historical trades
    api_response = api_instance.get_trades_by_date_range(start_date, end_date, page_number, page_size, segment=segment)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PostTradeApi->get_trades_by_date_range: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **str**| Date from which trade history needs to be fetched. Date in YYYY-mm-dd format | 
 **end_date** | **str**| Date till which history needs needs to be fetched. Date in YYYY-mm-dd format | 
 **page_number** | **int**| Page number for which you want to fetch trade history  | 
 **page_size** | **int**| How many records you want for a page  | 
 **segment** | **str**| Segment for which data is requested can be from the following options EQ - Equity,   FO - Futures and Options,   COM  - Commodity,   CD - Currency Derivatives MF - Mutual Funds | [optional] 

### Return type

[**TradeHistoryResponse**](TradeHistoryResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

